#!/usr/bin/env python3

from __future__ import annotations

import struct
import unittest

from tools.decode_binary_resources import (
    decode_audio_clip,
    decode_audio_event,
    decode_game_properties,
)
from tools.halleyconfig import encode_lz4


def string(value: str) -> bytes:
    encoded = value.encode()
    return struct.pack("<I", len(encoded)) + encoded


class BinaryResourceTest(unittest.TestCase):
    def test_decodes_audio_event(self) -> None:
        payload = (
            struct.pack("<I", 1)
            + string("setVariable")
            + struct.pack("<i", 1)
            + string("weather")
            + struct.pack("<f", 0.5)
        )
        self.assertEqual(
            decode_audio_event(payload),
            {
                "actions": [
                    {
                        "type": "setVariable",
                        "scope": 1,
                        "variable": "weather",
                        "value": 0.5,
                    }
                ]
            },
        )

    def test_decodes_legacy_audio_clip(self) -> None:
        payload = (
            struct.pack("<I", 1)
            + string("play")
            + struct.pack("<i", 1)
            + string("sfx/test.ogg")
            + string("sfx")
            + struct.pack("<ffff", 0.9, 1.1, 0.9, 1.0)
            + struct.pack("<f", 0.25)
        )
        decoded = decode_audio_clip(payload)
        self.assertEqual(decoded["actions"][0]["clip"], "sfx/test.ogg")
        self.assertEqual(decoded["actions"][0]["group"], "sfx")
        self.assertAlmostEqual(decoded["actions"][0]["gain"][0], 0.9)
        self.assertAlmostEqual(decoded["actions"][0]["gain"][1], 1.1)

    def test_decodes_game_properties(self) -> None:
        raw = (
            struct.pack("<I", 0)
            + struct.pack("<I", 0)
            + struct.pack("<I", 0)
            + struct.pack("<I", 1)
            + string("tag")
        )
        self.assertEqual(
            decode_game_properties(encode_lz4(raw)),
            {
                "audioProperties": {
                    "switches": [],
                    "variables": [],
                    "buses": [],
                },
                "materialTags": ["tag"],
            },
        )

    def test_decodes_wargroove_legacy_audio_event(self) -> None:
        payload = (
            struct.pack("<I", 1)
            + string("play")
            + struct.pack("<i", 0)
            + b"\0\0"
            + struct.pack("<H", len("map_music"))
            + b"map_music"
            + struct.pack("<ffi", 1.0, 0.0, 1)
            + struct.pack("<fffff", 1.0, 1.0, 1.0, 1.0, 0.0)
            + b"\0\0"
        )
        decoded = decode_audio_event(payload)
        self.assertTrue(decoded["actions"][0]["legacy"])
        self.assertEqual(decoded["actions"][0]["object"], "map_music")
        self.assertEqual(decoded["actions"][0]["gain"], [1.0, 1.0])

    def test_decodes_wargroove_legacy_game_properties(self) -> None:
        raw = (
            struct.pack("<I", 1)
            + string("MusicType")
            + struct.pack("<I", 2)
            + string("Default")
            + string("Combat")
            + struct.pack("<I", 0)
            + struct.pack("<I", 1)
            + string("master")
            + struct.pack("<I", 2)
            + string("music")
            + struct.pack("<I", 0)
            + string("sfx")
            + struct.pack("<I", 0)
        )
        decoded = decode_game_properties(encode_lz4(raw))
        self.assertTrue(decoded["legacy"])
        self.assertEqual(
            decoded["audioProperties"]["buses"][0]["children"][0]["id"],
            "music",
        )


if __name__ == "__main__":
    unittest.main()
