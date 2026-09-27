#!/usr/bin/env python3

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.config_workspace import (
    _validate_texture_metadata,
    pack_workspace,
    unpack_workspace,
)
from tools.halleyconfig import decode_payload, encode_payload
from tools.halley_font import encode_hlif_rgba
from tools.halleypk import FormatError
from tools.halleypk import ASSET_TYPES, Entry, HalleyPack, pack_container


class ConfigWorkspaceTest(unittest.TestCase):
    def test_rejects_texture_metadata_dimension_mismatch(self) -> None:
        payload = encode_hlif_rgba(bytes((255, 255, 255, 255)), 1, 1)
        item = {
            "asset_type": "texture",
            "asset_name": "fontTex/test",
            "metadata": {
                "format": "rgba",
                "height": 2,
                "width": 1,
            },
        }
        with self.assertRaisesRegex(FormatError, "metadata mismatch"):
            _validate_texture_metadata(item, payload)

    def test_unpack_edit_pack_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "config.dat"
            workspace = root / "workspace"
            output = root / "rebuilt.dat"
            config = encode_payload({"en-GB": {"title": "Hello"}})
            opaque = b"\x01\x02opaque"
            entries = [
                (
                    Entry(
                        ASSET_TYPES.index("configFile"),
                        "configFile",
                        "strings/en-GB",
                        0,
                        0,
                        None,
                        b"\0\0\0\0",
                    ),
                    config,
                ),
                (
                    Entry(
                        ASSET_TYPES.index("audioClip"),
                        "audioClip",
                        "audio/test",
                        0,
                        0,
                        None,
                        b"\0\0\0\0",
                    ),
                    opaque,
                ),
            ]
            source.write_bytes(
                pack_container(
                    entries,
                    legacy_layout=False,
                    legacy_metadata=False,
                    iv=bytes.fromhex("00112233445566778899aabbccddeeff"),
                )
            )

            unpack_workspace(source, workspace)
            string_path = workspace / "configFile/strings/en-GB.json"
            data = json.loads(string_path.read_text(encoding="utf-8"))
            data["en-GB"]["title"] = "Changed"
            string_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            korean_path = workspace / "configFile/strings/ko-KR.json"
            korean_path.write_text(
                json.dumps({"ko-KR": {"title": "안녕하세요"}}, ensure_ascii=False, indent=2)
                + "\n",
                encoding="utf-8",
            )

            result = pack_workspace(workspace, output)
            self.assertEqual(result["entry_count"], 3)
            self.assertEqual(result["added_asset_count"], 1)
            self.assertEqual(result["added_assets"], ["strings/ko-KR"])
            rebuilt = HalleyPack(output)
            config_entry = next(
                entry
                for entry in rebuilt.entries
                if entry.asset_type_name == "configFile" and entry.name == "strings/en-GB"
            )
            korean_entry = next(
                entry
                for entry in rebuilt.entries
                if entry.asset_type_name == "configFile" and entry.name == "strings/ko-KR"
            )
            audio_entry = next(
                entry
                for entry in rebuilt.entries
                if entry.asset_type_name == "audioClip"
            )
            self.assertEqual(
                decode_payload(rebuilt.payload(config_entry))["en-GB"]["title"],
                "Changed",
            )
            self.assertEqual(
                decode_payload(rebuilt.payload(korean_entry))["ko-KR"]["title"],
                "안녕하세요",
            )
            self.assertEqual(rebuilt.payload(audio_entry), opaque)


if __name__ == "__main__":
    unittest.main()
