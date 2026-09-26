#!/usr/bin/env python3
"""Build a continuity-first terminology batch from local language resources."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# WG1 source stays as raw unpacked binary; use the project's direct legacy
# ConfigFile decode as a readable terminology reference.
WG1_PATH = (
    ROOT
    / "work/docs/analysis/wargroove1-config-readable"
    / "strings/ko-KR.json"
)
WORK = ROOT / "work/Wargroove 2/1.2.x/config"
OUT = ROOT / "work/Wargroove 2/1.2.x"
REVIEW = ROOT / "work/docs/review"
TRANSLATION = WORK

# These are context changes in Wargroove 2, not spelling inconsistencies.
# The original Wargroove 1 terms remain in the glossary for continuity review.
CONTEXT_OVERRIDES = {
    "character_darkmercia_title": "여왕의 그림자",
    "character_emeric_title": "대마법사 - 왕실 고문",
    "character_generic_soldier3_name": "산적",
    "character_greenfinger_name": "자완",
    "character_greenfinger_title": "플로란 부족의 그린핑거",
    "character_koji_title": "헤븐송의 왕자",
    "character_mercival_name": "머시벌 2세",
    "character_mercival_title": "체리스톤의 선왕",
    "character_nuru_title": "외계에서 온 방문자",
    "character_ragna_title": "펠하임 최고의 사령관",
    "character_ryota_title": "늠름한 제독",
    "character_sedge_title": "가학적인 사냥꾼",
    "character_sigrid_title": "서부의 하이 뱀파이어",
    "character_valder_title": "대강령술사 - 펠하임의 군주",
    "character_vesper_title": "반려동물 납치 전과자",
}

QUALITY_OVERRIDES = {
    "operator_different": "아님",
    "operator_greater": "초과",
    "operator_less": "미만",
    "turn_n": "턴 {0}",
    "ui_map_day": "턴 {0}",
    "ui_cutscene_emote_cat": "에니드 눕기",
    "ui_cutscene_emote_catappears": "에니드 등장",
    "ui_cutscene_emote_catsit": "에니드 앉기",
    "ui_cutscene_emote_catstop": "에니드 그루밍 종료",
    "ui_cutscene_emote_pet": "쓰다듬기",
    "ui_cutscene_sfx_family_leaving_bushes": "울파와 쌍둥이가 수풀을 빠져나감",
    "ui_cutscene_sfx_family_leaving_cactus": "울파와 쌍둥이가 선인장을 빠져나감",
    "ui_cutscene_sfx_treasure_stolen": "골드 도난",
    "wg2_a1m1_cry_for_help_cutscene_a1m1_scene_1_intro_dialog_023_text": "머시아, 오랜만이야!",
    "wg2_a1m1_cry_for_help_cutscene_a1m1_scene_1_intro_dialog_055_text": "자세한 사정은 저도 듣지 못했습니다.[short_pause] [wavy]사적인 일이라는 것만[wavy] 압니다.",
    "wg2_a1m1_cry_for_help_cutscene_a1m1_scene_1_intro_dialog_085_text": "뭐?! [shaking]안 무섭거든!",
    "wg2_a1m1_cry_for_help_cutscene_a1m1_scene_1_intro_dialog_134_text": "[shaking]역사상 최고의 파자마 파티가 될 거야!",
    "wg2_a2m1_the_dead_of_night_trigger_talk_to_vesper_action_012_002": "[wavy]아이고...",
    "wg2_a3m1_bottom_of_the_world_cutscene_air_campaign_act_3_map_1_intro_dialog_008_text": "[wavy]말도 안 돼!",
    "wg2_forests_edge_trigger_initial_map_setup_intro_vesper_action_000_002": "[colour:purple][instant]대지가[shaking] 축축한[shaking] 감옥으로[scared][short_pause] [instant]변하면,[scared] 그녀가[instant] 끈질기게[shaking]--[shaking]신음하는 소리를 들을 수 있지.",
}


def load(path: Path, language: str | None = None) -> dict[str, str]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if "root" in value:
        value = value["root"]
    if language is not None:
        value = value[language]
    elif "ko-KR" in value:
        value = value["ko-KR"]
    return value


def load_resource_language(language: str) -> dict[str, str]:
    merged: dict[str, str] = {}
    for path in sorted((WORK / f"reference-json/{language}").glob("*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))[language]
        merged.update(value)
    return merged


def strip_legacy(value: str | None) -> str:
    if value is None:
        return ""
    return value[2:] if value.startswith("S:") else value


def is_term(key: str) -> bool:
    return key.startswith(
        (
            "character_",
            "faction_name_",
            "unit_name_",
            "structure_name_",
            "groove_name_",
        )
    )


def category(key: str) -> str:
    if key.startswith("character_"):
        return "character"
    if key.startswith("faction_name_"):
        return "faction"
    if key.startswith("unit_name_"):
        return "unit"
    if key.startswith("structure_name_"):
        return "structure"
    return "groove"


def build() -> tuple[list[dict[str, str]], dict[str, str]]:
    wg1 = load(WG1_PATH)
    languages = {
        lang: load_resource_language(lang)
        for lang in ("en-GB", "ja-JP", "zh-Hans", "ko-KR")
    }
    keys = sorted(
        {
            key
            for source in (*languages.values(), wg1)
            for key in source
            if is_term(key) or key in QUALITY_OVERRIDES
        }
    )
    rows: list[dict[str, str]] = []
    draft: dict[str, str] = {}
    for key in keys:
        ko_wg1 = strip_legacy(wg1.get(key))
        ko_nsw = languages["ko-KR"].get(key, "")
        proposed = ""
        status = "untranslated"
        notes = ""
        if key in QUALITY_OVERRIDES:
            proposed = QUALITY_OVERRIDES[key]
            status = "approved-quality"
            notes = "NSW resource의 명백한 미번역/잘못된 UI 문자열 수정"
        elif ko_wg1 and ko_nsw and ko_wg1 != ko_nsw:
            if key in CONTEXT_OVERRIDES:
                proposed = CONTEXT_OVERRIDES[key]
                status = "approved-context"
                notes = "WG2 영어 문맥과 NSW 번역이 WG1의 설명/칭호를 갱신"
            else:
                status = "blocked"
                notes = "Wargroove 1 공식 용어와 NSW WG2 번역이 다름"
        elif ko_wg1:
            proposed = ko_wg1
            status = "draft"
            notes = "Wargroove 1 공식 한국어 우선"
        elif ko_nsw:
            proposed = ko_nsw
            status = "draft"
            notes = "NSW WG2 번역을 Windows WG2 초안으로 사용"
        if proposed and status in ("draft", "approved-context", "approved-quality"):
            draft[key] = proposed
        rows.append(
            {
                "key": key,
                "category": category(key),
                "en": languages["en-GB"].get(key, ""),
                "ja": languages["ja-JP"].get(key, ""),
                "zh-Hans": languages["zh-Hans"].get(key, ""),
                "ko-wg1": ko_wg1,
                "ko-nsw": ko_nsw,
                "ko-proposed": proposed,
                "status": status,
                "notes": notes,
            }
        )
    return rows, draft


def main() -> None:
    rows, draft = build()
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    TRANSLATION.mkdir(parents=True, exist_ok=True)

    glossary_path = OUT / "wg2-terminology.tsv"
    with glossary_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    translation_path = TRANSLATION / "translation-draft.json"
    translation_path.write_text(
        json.dumps({"ko-KR": draft}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    blocked = [row for row in rows if row["status"] == "blocked"]
    drafted = [row for row in rows if row["status"] in ("draft", "approved-context")]
    context = [row for row in rows if row["status"] == "approved-context"]
    quality = [row for row in rows if row["status"] == "approved-quality"]
    untranslated = [row for row in rows if row["status"] == "untranslated"]
    report = [
        "# Translation Batch 001: Continuity Terms",
        "",
        "Date: 2026-09-26",
        "",
        "Scope: character names/titles, factions, unit names, structures, and grooves.",
        "",
        "Sources:",
        "- Wargroove 1 official Korean JSON from `references/Nexus/ModPacker-Wargoove-results/`.",
        "- NSW Wargroove 2 `ko-KR` resources decoded from `references/posts/WG2_KR/romfs/config.dat`.",
        "- NSW Wargroove 2 English, Japanese, and Simplified Chinese resources.",
        "",
        "## Result",
        "",
        f"- Draft terms: {len(drafted)}",
        f"- Context decisions recorded: {len(context)}",
        f"- Quality corrections recorded: {len(quality)}",
        f"- Blocked conflicts requiring review: {len(blocked)}",
        f"- Untranslated or missing source terms: {len(untranslated)}",
        f"- Candidate JSON: `{translation_path}`",
        f"- Glossary: `{glossary_path}`",
        "",
        "The candidate JSON records the first terminology decisions and is still",
        "a translation draft. It is not a release package; Windows runtime and",
        "font rendering tests are still required.",
        "",
        "## Remaining Review",
        "",
    ]
    if not blocked:
        report.append("- No unresolved conflicts in this batch.")
    for row in blocked:
        report.append(
            f"- `{row['key']}`: WG1=`{row['ko-wg1']}`; NSW=`{row['ko-nsw']}`. "
            f"English=`{row['en']}`; Japanese=`{row['ja']}`; Chinese=`{row['zh-Hans']}`."
        )
    (REVIEW / "batch-001-terminology.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
