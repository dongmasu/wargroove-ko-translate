#!/usr/bin/env python3
"""Regression checks for generated Korean translation resources."""

from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work/Wargroove 2/1.2.x/config"
SOURCE = WORK / "configFile/strings"
DRAFT = WORK / "translation-draft.json"
GENERATED = WORK / "configFile/strings"
FORMAT_TOKEN = re.compile(r"\{\d+\}")
DOCUMENTED_MISSING_KEYS = {
    "credits_firefalcom",
    "show_next_unit",
    "start_of_turn_p1_touch",
    "start_of_turn_p2_touch",
    "start_of_turn_p3_touch",
    "start_of_turn_p4_touch",
    "touch_anywhere",
    "ui_conflict_choose_first",
    "ui_conflict_choose_second",
    "ui_credits_close",
    "ui_export_save",
    "ui_fix_conflict_message",
    "ui_fix_conflict_title",
    "ui_import_confirmation_message",
    "ui_import_confirmation_title",
    "ui_import_error_message",
    "ui_import_error_title",
    "ui_import_save",
    "ui_no_tooltip_touch",
    "ui_tutorial_animation_name_zoom",
    "waiting_for_cloud",
    "wg2_tut_1_zoom_body",
    "wg2_tut_1_zoom_title",
}


def merge_language(language: str) -> dict[str, str]:
    merged: dict[str, str] = {}
    for path in sorted(SOURCE.glob(f"{language}*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        values = document[language]
        merged.update({key: value for key, value in values.items() if isinstance(value, str)})
    return merged


def merge_generated() -> dict[str, str]:
    merged: dict[str, str] = {}
    for path in sorted(GENERATED.glob("ko-KR*.json")):
        values = json.loads(path.read_text(encoding="utf-8"))["ko-KR"]
        merged.update({key: value for key, value in values.items()})
    return merged


class TranslationResourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.english = merge_language("en-GB")
        cls.korean = merge_generated()
        cls.draft = json.loads(DRAFT.read_text(encoding="utf-8"))["ko-KR"]

    def test_draft_keys_exist_in_source_resources(self) -> None:
        missing = sorted(set(self.draft) - set(self.korean))
        self.assertEqual(missing, [])

    def test_draft_preserves_format_tokens(self) -> None:
        mismatches = []
        for key in self.draft:
            source_tokens = Counter(FORMAT_TOKEN.findall(self.english.get(key, "")))
            target_tokens = Counter(FORMAT_TOKEN.findall(self.korean.get(key, "")))
            if source_tokens != target_tokens:
                mismatches.append((key, sorted(source_tokens.elements()), sorted(target_tokens.elements())))
        self.assertEqual(mismatches, [])

    def test_generated_covers_english_except_documented_missing_keys(self) -> None:
        missing = set(self.english) - set(self.korean)
        self.assertEqual(missing, DOCUMENTED_MISSING_KEYS)

    def test_generated_key_count_includes_structural_additions(self) -> None:
        merged = merge_language("ko-KR")
        self.assertTrue(set(merged).issubset(self.korean))
        self.assertEqual(len(self.korean), 15198)


if __name__ == "__main__":
    unittest.main()
