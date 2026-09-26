#!/usr/bin/env python3
"""Round-trip a Halley config.dat through a readable workspace."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from tools.halleyconfig import (
        ConfigFormatError,
        Writer,
        decode_lz4,
        decode_payload,
        encode_lz4,
    )
    from tools.halleypk import ASSET_TYPES, Entry, FormatError, HalleyPack, pack_container
    from tools.decode_binary_resources import (
        DecodeError,
        DECODERS,
        decode_opaque_structured,
    )
except ModuleNotFoundError:
    from halleyconfig import ConfigFormatError, Writer, decode_lz4, decode_payload, encode_lz4
    from halleypk import ASSET_TYPES, Entry, FormatError, HalleyPack, pack_container
    from decode_binary_resources import DecodeError, DECODERS, decode_opaque_structured


MANIFEST_NAME = "workspace.json"


def _decode_binary_json(asset_type: str, payload: bytes) -> dict[str, Any]:
    decoder = DECODERS.get(asset_type)
    if decoder is None:
        decoded = decode_opaque_structured(asset_type, payload)
    else:
        try:
            decoded = decoder(payload)
        except DecodeError as error:
            decoded = decode_opaque_structured(asset_type, payload)
            decoded["decodeError"] = str(error)
    return {
        "_assetType": asset_type,
        "_decoded": decoded,
        "_payloadHex": payload.hex(),
    }


def _safe_relative(asset_type: str, name: str, suffix: str) -> Path:
    relative = PurePosixPath(asset_type) / PurePosixPath(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise FormatError(f"unsafe asset path {name!r}")
    # Asset names may legitimately contain extensions and may coexist with
    # the extensionless form (for example, CF_Logo and CF_Logo.png).
    return Path(*relative.parts[:-1]) / (relative.name + suffix)


def _unwrap(payload: bytes) -> tuple[bytes, dict[str, Any]]:
    if payload[:4] == b"LZ4\0":
        return decode_lz4(payload), {
            "compression": "lz4",
            "wrapper_prefix": "",
        }
    if len(payload) >= 10 and payload[8:10] in {b"x\x01", b"x\x5e", b"x\x9c", b"x\xda"}:
        return zlib.decompress(payload[8:]), {
            "compression": "zlib",
            "wrapper_prefix": payload[:8].hex(),
        }
    return payload, {
        "compression": "raw",
        "wrapper_prefix": "",
    }


def _wrap(payload: bytes, compression: str, wrapper_prefix: str = "") -> bytes:
    if compression == "lz4":
        return encode_lz4(payload)
    if compression == "zlib":
        prefix = bytes.fromhex(wrapper_prefix)
        if len(prefix) != 8:
            raise FormatError("zlib workspace entry has an invalid wrapper prefix")
        return prefix + zlib.compress(payload)
    if compression == "raw":
        return payload
    raise FormatError(f"unsupported workspace compression {compression!r}")


def unpack_workspace(pack_path: Path, workspace: Path) -> dict[str, Any]:
    if workspace.exists() and any(workspace.iterdir()):
        raise FormatError(f"refusing to overwrite non-empty workspace: {workspace}")

    pack = HalleyPack(pack_path)
    workspace.mkdir(parents=True, exist_ok=True)
    files: list[dict[str, Any]] = []

    for entry in pack.entries:
        packed = pack.payload(entry)
        payload, wrapper = _unwrap(packed)
        is_config = entry.asset_type_name == "configFile"
        suffix = ".json"
        relative = _safe_relative(entry.asset_type_name, entry.name, suffix)
        destination = workspace / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        item: dict[str, Any] = {
            "asset_type": entry.asset_type_name,
            "asset_name": entry.name,
            "path": str(relative),
            "metadata": entry.metadata,
            "metadata_raw": entry.metadata_raw.hex(),
            "compression": wrapper["compression"],
            "wrapper_prefix": wrapper["wrapper_prefix"],
            "format": "config-json" if is_config else "opaque-binary",
            "packed_bytes": len(packed),
            "payload_bytes": len(payload),
            "payload_sha256": hashlib.sha256(payload).hexdigest(),
        }
        if is_config:
            try:
                decoded = decode_payload(packed)
                raw, _ = _unwrap(packed)
                item["config_version"] = struct.unpack_from("<i", raw, 0)[0]
            except ConfigFormatError as error:
                item["format"] = "binary-json"
                item["decode_error"] = str(error)
                destination.write_text(
                    json.dumps(_decode_binary_json(entry.asset_type_name, payload), ensure_ascii=False, indent=2)
                    + "\n",
                    encoding="utf-8",
                )
            else:
                destination.write_text(
                    json.dumps(decoded, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
        else:
            destination.write_text(
                json.dumps(_decode_binary_json(entry.asset_type_name, payload), ensure_ascii=False, indent=2)
                + "\n",
                encoding="utf-8",
            )
            item["format"] = "binary-json"
        files.append(item)

    manifest = {
        "format": 1,
        "source": str(pack_path),
        "source_sha256": hashlib.sha256(pack_path.read_bytes()).hexdigest(),
        "container": pack.magic,
        "iv": pack.iv.hex(),
        "legacy_layout": pack.legacy_layout,
        "legacy_metadata": pack.legacy_metadata,
        "entry_count": len(files),
        "files": files,
    }
    (workspace / MANIFEST_NAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def _encode_config(root: dict[str, Any], item: dict[str, Any]) -> bytes:
    version = int(item.get("config_version", 3))
    writer = Writer()
    writer.i32(version)
    if version == 3:
        writer.boolean(True)
    writer.node(root)
    return _wrap(bytes(writer.data), item["compression"], item.get("wrapper_prefix", ""))


def _discover_added_files(
    workspace: Path, files: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    indexed_paths = {str(item["path"]) for item in files}
    templates: dict[str, dict[str, Any]] = {}
    for item in files:
        templates.setdefault(item["asset_type"], item)

    additions: list[dict[str, Any]] = []
    for source_path in sorted(workspace.rglob("*.json")):
        relative = source_path.relative_to(workspace)
        relative_text = str(relative)
        if relative_text in indexed_paths or relative.name == MANIFEST_NAME:
            continue
        if len(relative.parts) < 2 or relative.parts[0] not in ASSET_TYPES:
            continue

        asset_type = relative.parts[0]
        template = templates.get(asset_type)
        if template is None:
            raise FormatError(
                f"cannot infer metadata for added asset type {asset_type!r}: "
                f"{source_path}"
            )
        document = json.loads(source_path.read_text(encoding="utf-8"))
        if asset_type == "configFile":
            item_format = (
                "binary-json" if "_payloadHex" in document else "config-json"
            )
        elif "_payloadHex" in document:
            item_format = "binary-json"
        else:
            raise FormatError(
                f"added non-config asset must contain _payloadHex: {source_path}"
            )

        asset_name = str(PurePosixPath(*relative.parts[1:]).with_suffix(""))
        item = {
            "asset_type": asset_type,
            "asset_name": asset_name,
            "path": relative_text,
            "metadata": template.get("metadata"),
            "metadata_raw": template["metadata_raw"],
            "compression": template["compression"],
            "wrapper_prefix": template.get("wrapper_prefix", ""),
            "format": item_format,
            "packed_bytes": 0,
            "payload_bytes": 0,
            "payload_sha256": "",
        }
        if "config_version" in template:
            item["config_version"] = template["config_version"]
        additions.append(item)
    return additions


def pack_workspace(workspace: Path, output: Path) -> dict[str, Any]:
    manifest_path = workspace / MANIFEST_NAME
    if output.exists():
        raise FormatError(f"refusing to overwrite existing output: {output}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("format") != 1:
        raise FormatError("unsupported workspace manifest version")

    files = list(manifest["files"])
    additions = _discover_added_files(workspace, files)
    files.extend(additions)
    entries: list[tuple[Entry, bytes]] = []
    for item in files:
        metadata_raw = bytes.fromhex(item["metadata_raw"])
        asset_type = item["asset_type"]
        if asset_type not in ASSET_TYPES:
            raise FormatError(f"unknown asset type {asset_type!r}")
        entry = Entry(
            asset_type=ASSET_TYPES.index(asset_type),
            asset_type_name=asset_type,
            name=item["asset_name"],
            offset=0,
            size=0,
            metadata=item.get("metadata"),
            metadata_raw=metadata_raw,
        )
        source_path = workspace / item["path"]
        if not source_path.is_file():
            raise FormatError(f"workspace asset is missing: {source_path}")
        if item["format"] == "config-json":
            root = json.loads(source_path.read_text(encoding="utf-8"))
            content = _encode_config(root, item)
        elif item["format"] == "binary-json":
            document = json.loads(source_path.read_text(encoding="utf-8"))
            try:
                payload = bytes.fromhex(document["_payloadHex"])
            except (KeyError, TypeError, ValueError) as error:
                raise FormatError(
                    f"binary JSON has an invalid _payloadHex: {source_path}"
                ) from error
            content = _wrap(
                payload,
                item["compression"],
                item.get("wrapper_prefix", ""),
            )
        else:
            content = _wrap(
                source_path.read_bytes(),
                item["compression"],
                item.get("wrapper_prefix", ""),
            )
        entries.append((entry, content))

    version = 1 if manifest["container"] == "v1" else 2
    data = pack_container(
        entries,
        bool(manifest["legacy_layout"]),
        bool(manifest["legacy_metadata"]),
        version=version,
        iv=bytes.fromhex(manifest["iv"]),
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    verified = HalleyPack(output)
    if len(verified.entries) != len(entries):
        raise FormatError("workspace output entry count mismatch")
    result = {
        "workspace": str(workspace),
        "output": str(output),
        "entry_count": len(verified.entries),
        "added_asset_count": len(additions),
        "added_assets": [item["asset_name"] for item in additions],
        "output_sha256": hashlib.sha256(data).hexdigest(),
    }
    output.with_suffix(".json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    unpack = commands.add_parser("unpack")
    unpack.add_argument("pack", type=Path)
    unpack.add_argument("workspace", type=Path)
    pack = commands.add_parser("pack")
    pack.add_argument("workspace", type=Path)
    pack.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        result = (
            unpack_workspace(args.pack, args.workspace)
            if args.command == "unpack"
            else pack_workspace(args.workspace, args.output)
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ConfigFormatError, FormatError, OSError, json.JSONDecodeError) as error:
        print(f"error: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
