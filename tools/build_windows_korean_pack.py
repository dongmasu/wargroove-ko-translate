#!/usr/bin/env python3
"""Build and verify a Windows Wargroove 2 config.dat Koreanization pack."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

from halleypk import ASSET_TYPES, Entry, HalleyPack, pack_container


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = ROOT / "references/Wargroove 2/assets/config.dat"
DEFAULT_RESOURCES = ROOT / "work/Wargroove 2/1.2.x/config/strings"
DEFAULT_OUTPUT = (
    ROOT
    / "dist/Wargroove 2/1.2.x"
    / date.today().strftime("%Y%m%d")
    / "config.dat"
)


def build(base: Path, resources: Path, output: Path) -> dict[str, object]:
    if output.exists():
        raise ValueError(f"refusing to overwrite existing output: {output}")

    source = HalleyPack(base)
    config_type = ASSET_TYPES.index("configFile")
    metadata_source = next(
        entry
        for entry in source.entries
        if entry.asset_type == config_type and entry.name == "strings/en-GB"
    )

    entries = [(entry, source.payload(entry)) for entry in source.entries]
    added_names: list[str] = []
    for payload_path in sorted(resources.glob("ko-KR*.bin")):
        suffix = payload_path.stem
        asset_name = f"strings/{suffix}"
        if any(
            entry.asset_type_name == "configFile" and entry.name == asset_name
            for entry in source.entries
        ):
            raise ValueError(f"asset already exists in base pack: {asset_name}")
        entries.append(
            (
                Entry(config_type, "configFile", asset_name, 0, 0, {}, metadata_source.metadata_raw),
                payload_path.read_bytes(),
            )
        )
        added_names.append(asset_name)

    if len(added_names) != 24:
        raise ValueError(f"expected 24 Korean resources, found {len(added_names)}")

    output_data = pack_container(
        entries,
        source.legacy_layout,
        source.legacy_metadata,
        version=1,
        iv=source.iv,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(output_data)

    verified = HalleyPack(output)
    expected_count = len(source.entries) + len(added_names)
    if len(verified.entries) != expected_count:
        raise ValueError(
            f"entry count mismatch: expected {expected_count}, got {len(verified.entries)}"
        )
    for asset_name, payload_path in zip(added_names, sorted(resources.glob("ko-KR*.bin"))):
        entry = next(
            entry
            for entry in verified.entries
            if entry.asset_type_name == "configFile" and entry.name == asset_name
        )
        if verified.payload(entry) != payload_path.read_bytes():
            raise ValueError(f"payload verification failed: {asset_name}")

    digest = hashlib.sha256(output_data).hexdigest()
    manifest = {
        "base": str(base),
        "output": str(output),
        "base_sha256": hashlib.sha256(base.read_bytes()).hexdigest(),
        "output_sha256": digest,
        "base_entry_count": len(source.entries),
        "output_entry_count": len(verified.entries),
        "added_assets": added_names,
        "encrypted_payload": verified.iv != bytes(16),
    }
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, default=DEFAULT_BASE)
    parser.add_argument("--resources", type=Path, default=DEFAULT_RESOURCES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    manifest = build(args.base, args.resources, args.output)
    manifest_path = args.output.with_suffix(".json")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
