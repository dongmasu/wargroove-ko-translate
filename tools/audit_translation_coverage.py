#!/usr/bin/env python3
"""Audit all generated Korean string resources against source languages."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work/Wargroove 2/1.2.x/config"
SOURCE = WORK / "reference-json"
GENERATED = WORK / "strings"
OUTPUT = ROOT / "work/docs/review/translation-coverage-2026-09-26.md"
MARKUP = re.compile(r"\{\d+\}|\[[^\]]+\]")
PLACEHOLDER = re.compile(r"\{\d+\}|\[\d+\]")


def load(path: Path, language: str) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))[language]


def source_resource_paths(language: str) -> list[Path]:
    base = SOURCE / language / f"{language}.json"
    return [base, *sorted((SOURCE / language).glob(f"{language}_*.json"))]


def generated_path(source_path: Path) -> Path:
    return GENERATED / source_path.name


def tokens(value: object) -> Counter[str]:
    return Counter(MARKUP.findall(value)) if isinstance(value, str) else Counter()


def placeholders(value: object) -> Counter[str]:
    return Counter(PLACEHOLDER.findall(value)) if isinstance(value, str) else Counter()


def main() -> None:
    rows: list[dict[str, object]] = []
    total_keys = 0
    total_missing = 0
    total_empty = 0
    total_same = 0
    total_placeholder_mismatch = 0
    total_markup_difference = 0

    for english_path in source_resource_paths("en-GB"):
        if english_path.name == "en-GB.json":
            resource = "root"
            ko_path = SOURCE / "ko-KR/ko-KR.json"
        else:
            resource = english_path.name.removeprefix("en-GB_").removesuffix(".json")
            ko_path = SOURCE / "ko-KR" / f"ko-KR_{resource}.json"
        generated = generated_path(ko_path)
        english = load(english_path, "en-GB")
        korean = load(generated, "ko-KR")
        missing = [key for key in english if key not in korean]
        empty = [key for key, value in korean.items() if value == ""]
        same = [
            key
            for key, value in english.items()
            if value and korean.get(key) == value
        ]
        placeholder_mismatches = [
            key
            for key, value in english.items()
            if key in korean and placeholders(value) != placeholders(korean[key])
        ]
        markup_differences = [
            key
            for key, value in english.items()
            if key in korean and tokens(value) != tokens(korean[key])
        ]
        row = {
            "resource": resource,
            "keys": len(korean),
            "missing": len(missing),
            "empty": len(empty),
            "same": len(same),
            "placeholder_mismatch": len(placeholder_mismatches),
            "markup_difference": len(markup_differences),
            "missing_keys": missing,
            "empty_keys": empty,
            "same_keys": same,
            "placeholder_mismatch_keys": placeholder_mismatches,
            "markup_difference_keys": markup_differences,
        }
        rows.append(row)
        total_keys += len(korean)
        total_missing += len(missing)
        total_empty += len(empty)
        total_same += len(same)
        total_placeholder_mismatch += len(placeholder_mismatches)
        total_markup_difference += len(markup_differences)

    lines = [
        "# Translation Coverage Audit",
        "",
        "Date: 2026-09-26",
        "",
        "Scope: all generated Windows Wargroove 2 Korean string resources.",
        "The audit compares the generated resource JSON against NSW English and",
        "checks placeholders and markup tags. Identical values are findings for review,",
        "not automatic translation errors; they include punctuation, numbers,",
        "credits, language names, placeholders, and audio/developer identifiers.",
        "",
        "## Summary",
        "",
        f"- Resources audited: {len(rows)}",
        f"- Generated key entries: {total_keys}",
        f"- Missing English keys: {total_missing}",
        f"- Empty Korean values: {total_empty}",
        f"- English/Korean identical values: {total_same}",
        f"- Placeholder mismatches: {total_placeholder_mismatch}",
        f"- Markup tag differences requiring review: {total_markup_difference}",
        "",
        "## Per Resource",
        "",
        "| Resource | Keys | Missing | Empty | Identical | Placeholder mismatch | Markup differences |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['resource']}` | {row['keys']} | {row['missing']} | "
            f"{row['empty']} | {row['same']} | {row['placeholder_mismatch']} | "
            f"{row['markup_difference']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Missing keys and placeholder mismatches must be zero before release.",
            "- Empty values remain deferred only when the source value is also",
            "  intentionally blank or its runtime role is unknown.",
            "- Markup tag differences are retained for semantic/UI review because",
            "  Halley tags may be toggles or explicit open/close pairs.",
            "- Identical values were separately classified in the review reports.",
            "- This audit does not replace Windows runtime checks for clipping,",
            "  font rendering, language selection, or fallback behavior.",
        ]
    )
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:16]))


if __name__ == "__main__":
    main()
