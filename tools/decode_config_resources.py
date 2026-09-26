#!/usr/bin/env python3
"""Decode Wargroove ConfigFile assets into readable JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from halleyconfig import decode_payload
from halleypk import HalleyPack


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK = ROOT / "references/Wargroove 2/assets/config.dat"
DEFAULT_OUTPUT = ROOT / "work/docs/analysis/wargroove2-config-readable"


def write_decoded(source: Path, relative: Path, data: bytes, output: Path) -> dict[str, object]:
    output_path = (output / relative).with_suffix(".json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    decoded = decode_payload(data)
    output_path.write_text(
        json.dumps(decoded, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "source": str(source),
        "output": str(output_path.relative_to(output)),
        "bytes": len(data),
    }


def decode_pack(pack_path: Path, output: Path) -> dict[str, object]:
    pack = HalleyPack(pack_path)
    entries = [entry for entry in pack.entries if entry.asset_type_name == "configFile"]
    if not entries:
        raise ValueError(f"no configFile assets found in {pack_path}")
    files: list[dict[str, object]] = []
    for entry in sorted(entries, key=lambda item: item.name):
        files.append(
            {
                "asset": entry.name,
                **write_decoded(
                    pack_path,
                    Path(entry.name),
                    pack.payload(entry),
                    output,
                ),
            }
        )

    manifest = {
        "source": str(pack_path),
        "output": str(output),
        "resource_type": "configFile",
        "payload_count": len(files),
        "files": files,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def decode_source_directory(source: Path, output: Path) -> dict[str, object]:
    config_root = source / "configFile"
    payloads = sorted(config_root.rglob("*.bin"))
    if not payloads:
        raise ValueError(f"no ConfigFile .bin payloads found under {config_root}")
    files = [
        write_decoded(
            payload_path,
            payload_path.relative_to(config_root),
            payload_path.read_bytes(),
            output,
        )
        for payload_path in payloads
    ]
    manifest = {
        "source": str(source),
        "output": str(output),
        "resource_type": "configFile",
        "payload_count": len(files),
        "files": files,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Decode Halley ConfigFile assets from a pack into JSON."
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--pack", type=Path, default=DEFAULT_PACK)
    source.add_argument("--source-dir", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    manifest = (
        decode_source_directory(args.source_dir, args.output)
        if args.source_dir
        else decode_pack(args.pack, args.output)
    )
    print(
        f"Decoded {manifest['payload_count']} ConfigFile payloads "
        f"to {manifest['output']}"
    )


if __name__ == "__main__":
    main()
