#!/usr/bin/env python3
"""Small regression tests for the read-only HALLEYPK parser."""

from __future__ import annotations

import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from tools.halleypk import (
    AES_KEY,
    Entry,
    HalleyPack,
    FormatError,
    aes_cbc,
    cmd_payload_export,
    cmd_payload_import,
    pack_container,
)


def string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    return struct.pack("<I", len(encoded)) + encoded


def synthetic_pack() -> bytes:
    # One configFile entry with empty metadata (ConfigNode Undefined).
    index = (
        struct.pack("<I", 1)
        + struct.pack("<i", 2)
        + struct.pack("<i", 2)
        + struct.pack("<I", 1)
        + string("strings/ko-KR")
        + string("0:4")
        + struct.pack("<i", 0)
    )
    asset_db_start = 40
    compressed = zlib.compress(index)
    data_start = asset_db_start + len(compressed)
    packed_index = struct.pack("<Q", len(index)) + compressed
    data_start = asset_db_start + len(packed_index)
    header = b"HALLEYPK" + struct.pack("<16sQQ", b"\0" * 16, asset_db_start, data_start)
    return header + packed_index + b"test"


def synthetic_legacy_pack() -> bytes:
    # Legacy Wargroove 1 config layout: asset type, entry count, then entries.
    index = (
        struct.pack("<I", 1)
        + struct.pack("<i", 2)
        + struct.pack("<I", 1)
        + string("strings/ko-KR")
        + string("0:4")
        + struct.pack("<i", 0)
    )
    compressed = zlib.compress(index)
    packed_index = struct.pack("<Q", len(index)) + compressed
    data_start = 40 + len(packed_index)
    header = b"HALLEYPK" + struct.pack("<16sQQ", b"\0" * 16, 40, data_start)
    return header + packed_index + b"test"


class HalleyPackTest(unittest.TestCase):
    def test_aes_cbc_matches_nist_vector(self) -> None:
        key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
        plaintext = bytes.fromhex("00112233445566778899aabbccddeeff")
        ciphertext = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")
        original_key = AES_KEY
        try:
            import tools.halleypk as halleypk

            halleypk.AES_KEY = key
            self.assertEqual(aes_cbc(plaintext, bytes(16)), ciphertext)
            self.assertEqual(aes_cbc(ciphertext, bytes(16), decrypt=True), plaintext)
        finally:
            halleypk.AES_KEY = original_key

    def test_reads_encrypted_pack_and_roundtrips_payload(self) -> None:
        entry = Entry(2, "configFile", "strings/ko-KR", 0, 0, None, b"\0\0\0\0")
        source = pack_container(
            [(entry, b"0123456789abcdef")],
            legacy_layout=False,
            legacy_metadata=False,
            iv=bytes.fromhex("00112233445566778899aabbccddeeff"),
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "encrypted.dat"
            path.write_bytes(source)
            pack = HalleyPack(path)
            self.assertTrue(pack.manifest()["encrypted_payload"])
            self.assertEqual(pack.payload(pack.entries[0]), b"0123456789abcdef")

    def test_reads_entry_and_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.dat"
            path.write_bytes(synthetic_pack())
            pack = HalleyPack(path)
            self.assertEqual(pack.magic, "v1")
            self.assertEqual(len(pack.entries), 1)
            self.assertEqual(pack.entries[0].name, "strings/ko-KR")
            self.assertEqual(pack.payload(pack.entries[0]), b"test")

    def test_rejects_invalid_magic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.dat"
            path.write_bytes(b"not-a-pack")
            with self.assertRaises(FormatError):
                HalleyPack(path)

    def test_reads_legacy_entry_layout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "legacy.dat"
            path.write_bytes(synthetic_legacy_pack())
            pack = HalleyPack(path)
            self.assertEqual(pack.entries[0].asset_type_name, "configFile")
            self.assertEqual(pack.payload(pack.entries[0]), b"test")

    def test_replaces_existing_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.dat"
            output = Path(directory) / "output.dat"
            source.write_bytes(synthetic_pack())
            pack = HalleyPack(source)
            replacement = pack_container(
                [(pack.entries[0], b"changed")],
                pack.legacy_layout,
                pack.legacy_metadata,
            )
            replacement_pack = Path(directory) / "replacement.dat"
            replacement_pack.write_bytes(replacement)
            self.assertEqual(
                HalleyPack(replacement_pack).payload(HalleyPack(replacement_pack).entries[0]),
                b"changed",
            )

    def test_payload_hex_export_import_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            template = root / "font.json"
            raw = root / "font.bin"
            exported = root / "exported.bin"
            imported = root / "imported.json"
            template.write_text(
                '{"_assetType":"font","_payloadHex":"0001","_decoded":{"decoded":false}}\n',
                encoding="utf-8",
            )
            raw.write_bytes(b"Halley payload")

            cmd_payload_export(
                type(
                    "Args",
                    (),
                    {"source": template, "output": exported},
                )()
            )
            self.assertEqual(exported.read_bytes(), b"\x00\x01")

            cmd_payload_import(
                type(
                    "Args",
                    (),
                    {"template": template, "payload": raw, "output": imported},
                )()
            )
            document = json.loads(imported.read_text(encoding="utf-8"))
            self.assertEqual(bytes.fromhex(document["_payloadHex"]), b"Halley payload")
            self.assertEqual(document["_assetType"], "font")


if __name__ == "__main__":
    unittest.main()
