#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path

from tools.halleyconfig import decode_payload, encode_payload


ROOT = Path(__file__).resolve().parents[1]


class HalleyConfigTest(unittest.TestCase):
    def test_roundtrip_nested_config(self) -> None:
        root = {
            "ko-KR": {
                "name": "체리스톤",
                "enabled": True,
                "position": [3, 7],
                "items": ["검", "방패"],
            }
        }
        self.assertEqual(decode_payload(encode_payload(root)), root)

    def test_decodes_nsw_korean_resource(self) -> None:
        path = ROOT / "tests/fixtures/ko-KR.bin"
        root = decode_payload(path.read_bytes())
        self.assertIn("ko-KR", root)
        self.assertEqual(root["ko-KR"]["achievement_collect_all_stars_title"], "별처럼 빛나는 전술가")

    def test_decodes_wargroove1_legacy_resource(self) -> None:
        path = ROOT / "tests/fixtures/wg1-ko-KR.bin"
        root = decode_payload(path.read_bytes())
        self.assertIn("ko-KR", root)
        self.assertEqual(
            root["ko-KR"]["achievement_collect_all_stars_title"],
            "별처럼 빛나는 전술가",
        )


if __name__ == "__main__":
    unittest.main()
