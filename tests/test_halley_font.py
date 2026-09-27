#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from tools.halley_font import (
    HalleyFontError,
    decode_hlif_rgba,
    decode_hlif_single_channel,
    encode_hlif_rgba,
    encode_hlif_single_channel,
    generate_sdf,
    load_payload_json,
    parse_font_payload,
    serialize_font_payload,
)


ROOT = Path(__file__).parents[1]
FONT_JSON = ROOT / "src/Wargroove 2/1.2.x/ui/font/Wargroove Medium.json"
TEXTURE_JSON = ROOT / "src/Wargroove 2/1.2.x/ui/texture/fontTex/Wargroove Medium.json"


class HalleyFontTest(unittest.TestCase):
    def test_parses_and_round_trips_wargroove_medium(self) -> None:
        payload = load_payload_json(FONT_JSON)
        font = parse_font_payload(payload)
        self.assertEqual(font.name, "Wargroove Medium")
        self.assertEqual(font.image_name, "fontTex/Wargroove Medium")
        self.assertEqual(font.image_size, (256, 256))
        self.assertEqual(len(font.glyphs), 534)
        self.assertEqual(font.fallback, ("PixelMPlus", "Zpix", "AaCassiopeiaL1"))
        self.assertEqual(serialize_font_payload(font), payload)

    def test_decodes_reference_single_channel_hlif(self) -> None:
        payload = load_payload_json(TEXTURE_JSON)
        image = decode_hlif_single_channel(payload)
        self.assertEqual((image.width, image.height), (256, 256))
        self.assertEqual(len(image.pixels), 256 * 256)

    def test_encodes_and_decodes_single_channel_hlif(self) -> None:
        pixels = bytes([0, 10, 20, 30, 255, 4, 5, 6])
        payload = encode_hlif_single_channel(pixels, 4, 2)
        image = decode_hlif_single_channel(payload)
        self.assertEqual((image.width, image.height), (4, 2))
        self.assertEqual(image.pixels, pixels)

    def test_encodes_and_decodes_rgba_hlif(self) -> None:
        pixels = bytes([0, 0, 0, 0, 255, 255, 255, 255])
        payload = encode_hlif_rgba(pixels, 2, 1)
        image = decode_hlif_rgba(payload)
        self.assertEqual((image.width, image.height), (2, 1))
        self.assertEqual(image.pixels, pixels)

    def test_generates_single_channel_sdf(self) -> None:
        source = bytes([0, 0, 0, 0, 255, 255, 0, 0, 0])
        sdf = generate_sdf(source, 3, 3, 1.5)
        self.assertEqual(len(sdf), 9)
        self.assertGreater(sdf[4], 127)
        self.assertLess(sdf[0], 127)

    def test_sdf_threshold_preserves_antialiased_strokes(self) -> None:
        source = bytes([0, 1, 0])
        sdf = generate_sdf(source, 3, 1, 1.5, threshold=0)
        self.assertGreater(sdf[1], 127)

    def test_rejects_non_hex_json_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text(json.dumps({"_payloadHex": "not-hex"}), encoding="utf-8")
            with self.assertRaises(HalleyFontError):
                load_payload_json(path)


if __name__ == "__main__":
    unittest.main()
