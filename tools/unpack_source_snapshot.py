#!/usr/bin/env python3
"""Decrypt and decompress every asset in a Halley asset pack."""

from __future__ import annotations

import argparse
import json
import zlib
from pathlib import Path

try:
    from tools.halleyconfig import decode_lz4
    from tools.halleypk import HalleyPack
except ModuleNotFoundError:
    from halleyconfig import decode_lz4
    from halleypk import HalleyPack


ROOT = Path(__file__).resolve().parents[1]


def unpack_payload(payload: bytes) -> tuple[bytes, str]:
    if payload[:4] == b"LZ4\0":
        return decode_lz4(payload), "lz4"
    if len(payload) >= 10 and payload[8:10] in {b"x\x01", b"x\x5e", b"x\x9c", b"x\xda"}:
        return zlib.decompress(payload[8:]), "zlib"
    return payload, "raw"


def unpack_pack(pack_path: Path, output: Path) -> dict[str, object]:
    pack = HalleyPack(pack_path)
    files: list[dict[str, object]] = []
    for entry in pack.entries:
        packed_payload = pack.payload(entry)
        payload, compression = unpack_payload(packed_payload)
        relative = Path(entry.asset_type_name) / Path(entry.name).with_suffix(".bin")
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
        files.append(
            {
                "asset_type": entry.asset_type_name,
                "asset": entry.name,
                "output": str(relative),
                "compression": compression,
                "packed_bytes": len(packed_payload),
                "unpacked_bytes": len(payload),
            }
        )

    manifest = {
        "source": str(pack_path),
        "output": str(output),
        "container": pack.magic,
        "entry_count": len(files),
        "files": files,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Decrypt and decompress all assets from a Halley pack."
    )
    parser.add_argument("pack", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    manifest = unpack_pack(args.pack, args.output)
    print(
        f"Unpacked {manifest['entry_count']} assets to {manifest['output']}"
    )


if __name__ == "__main__":
    main()
