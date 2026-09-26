#!/usr/bin/env python3
"""Split the terminology draft into per-resource JSON and LZ4 payloads."""

from __future__ import annotations

import json
from pathlib import Path

from halleyconfig import encode_payload


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work/Wargroove 2/1.2.x/config"
SOURCE = WORK / "reference-json/ko-KR"
DRAFT = WORK / "translation-draft.json"
OUTPUT = WORK / "strings"

# These keys are absent from the NSW Korean resource but have unambiguous
# values or types. Blank/internal entries remain deferred for review.
MISSING_ADDITIONS: dict[str, dict[str, object]] = {
    "": {
        "ui_ugc_filter_players_1": "1",
        "ui_ugc_filter_players_2": "2",
        "ui_ugc_filter_players_3": "3",
        "ui_ugc_filter_players_4": "4",
    },
    "_campaign_air": {
        "wg2_a3m2_¤ΐж※Ħ※×§_cutscene_a3m2_scene_1_intro_dialog_070_text": "[wavy][slow]???",
        "wg2_a3m2_¤ΐж※Ħ※×§_trigger_player_destroys_growth_1_action_003_002": "???",
        "wg2_campaign_mapdescription_a3m2_¤ΐж※Ħ※×§": "???",
        "wg2_campaign_mapname_a3m2_¤ΐж※Ħ※×§": "???",
    },
    "_campaign_earth": {
        "wg2_campaign_mapobjective_e1m4_forgotten_halls": "          ",
        "wg2_campaign_mapobjective_e2m1_her_loyal_assistant": "          ",
        "wg2_campaign_mapobjective_e2m2_not_quite_ideal": "          ",
    },
    "_campaign_final": {
        "wg2_campaign_mapdescription_f3_high_noon": "          ",
        "wg2_campaign_mapdescription_f4_a_voice_from_beyond": "          ",
    },
    "_codex_commanders": {
        "character_caesar_age": 7,
        "character_emeric_age": 60,
        "character_greenfinger_age": 121,
        "character_koji_age": 13,
        "character_mercia_age": 24,
        "character_ryota_age": 30,
        "character_tenri_age": 49,
        "character_twins_age": 13,
        "character_valder_age": 37,
        "character_vesper_age": 39,
        "character_wulfar_age": 39,
        "character_elodie_age": "",
        "character_elodie_birthday": "",
        "character_elodie_birthplace": "",
        "character_vesper_birthday": "",
    },
    "_new_VO_lines": {
        "ui_cutscene_shout_nadia_die_ghost": "",
        "ui_cutscene_shout_nadia_die_no_battle": "",
        "ui_cutscene_shout_nadia_groove": "",
        "ui_cutscene_shout_nadia_groove_hit": "",
        "ui_cutscene_shout_nadia_groove_intro": "",
        "ui_cutscene_shout_nadia_groove_part1": "",
        "ui_cutscene_shout_nadia_groove_part2": "",
    },
    "_ui": {
        "boolean_false": False,
        "boolean_true": True,
        "turn_n_short": "턴 ",
    },
    "_wargroove2": {
        "character_donut_title": "",
        "character_fenris_title": "",
        "character_floran_captain_title": "",
        "character_lytra_flying_title": "",
        "character_lytra_no_harp_title": "",
        "character_rhomb_angry_title": "",
        "character_theWarship_title": "",
        "character_wulfar_pirate_title": "",
        "codex_unit_boarding_ship_critical_text": "",
        "ui_menu_singleplayer_campaign_final_desc": "            ",
        "ui_sector_properties_colour_tooltip": "",
        "ui_sector_properties_name_tooltip": "",
    },
    "_wargroove2_dev": {
        "wg2_between_trees_trigger_no_one_here_caesar_action_000_003": "caesar_growl",
        "wg2_between_trees_trigger_no_one_here_emeric_action_000_003": "emeric_hmm1",
        "wg2_cozy_fire_trigger_mystery_player_=_caesar_action_000_003": "ragna_what",
        "wg2_cozy_fire_trigger_mystery_player_=_caesar_action_001_003": "ragna_hmph",
        "wg2_lone_settlement_trigger_mystery_event_player_has_enough_gold_action_000_003": "koji_laugh",
        "wg2_lone_settlement_trigger_mystery_event_player_has_enough_gold_action_004_003": "koji_yeah",
        "wg2_secret_tower_trigger_finish_action_000_003": "elodie_laugh1",
        "wg2_the_castle_trigger_cutscene_new_action_001_003": "valder_no1",
        "wg2_the_castle_trigger_open_text_mercia_action_002_003": "valder_laugh",
        "wg2_the_castle_trigger_win_text_caesar_action_001_003": "caesar_barktwice",
        "wg2_the_heros_blessing_trigger_caesar_dialogue_action_000_003": "caesar_barktwice",
        "wg2_the_heros_blessing_trigger_caesar_dialogue_action_000_003a": "caesar_barktwice",
        "wg2_the_heros_blessing_trigger_dark_mercia_dialogue_action_000_003": "emeric_myqueen3",
        "wg2_the_heros_blessing_trigger_dark_mercia_dialogue_action_000_003a": "emeric_myqueen3",
        "wg2_the_heros_blessing_trigger_dark_mercia_dialogue_action_001_003": "darkmercia_yes",
        "wg2_the_heros_blessing_trigger_dark_mercia_dialogue_action_001_003a": "darkmercia_yes",
        "wg2_the_heros_blessing_trigger_mercival_opening_text_action_000_003": "mercival_ghost_laugh2",
        "wg2_the_heros_blessing_trigger_mercival_postblessing_text_action_000_003": "mercival_ghost_verywellthen",
        "wg2_the_heros_blessing_trigger_mercival_postco_caesar_action_000_003": "mercival_ghost_laugh1",
        "wg2_the_heros_blessing_trigger_mercival_postco_dark_mercia_action_000_003": "mercival_ghost_mylittlebluebird2",
        "wg2_the_heros_blessing_trigger_mercival_postco_dark_mercia_action_001_003": "mercival_ghost_laugh3",
        "wg2_the_heros_blessing_trigger_mercival_postco_emeric_action_000_003": "mercival_ghost_emeric",
        "wg2_the_heros_blessing_trigger_mercival_postco_end_action_000_003": "mercival_ghost_laugh3",
        "wg2_the_heros_blessing_trigger_mercival_postco_mercia_action_000_003": "mercival_ghost_mylittlebluebird1",
        "wg2_the_heros_blessing_trigger_mercival_postco_nadia_action_000_003": "mercival_ghost_greetings",
        "wg2_the_heros_blessing_trigger_mercival_postformation_text_action_002_003": "mercival_ghost_farewell",
        "wg2_the_heros_blessing_trigger_randomized_interlude_action_000_003": "tenri_agreed",
        "wg2_the_heros_blessing_trigger_randomized_interlude_action_000_003a": "tenri_agreed",
        "wg2_the_heros_blessing_trigger_randomized_interlude_action_001_003": "valder_very_well",
        "wg2_the_heros_blessing_trigger_randomized_interlude_action_001_003a": "valder_very_well",
        "wg2_the_heros_blessing_trigger_randomized_interlude_action_002_003": "nuru_seeya",
        "wg2_the_heros_blessing_trigger_randomized_interlude_action_002_003a": "nuru_seeya",
        "wg2_toll_station_trigger_commanderonly_event_action_002_003": "ryota_hmph1",
        "wg2_tutorial_trigger_nadia_is_attacked_action_000_003": "ragna_oh1",
        "wg2_tutorial_trigger_post_attack_action_000_003": "ragna_what",
        "wg2_tutorial_trigger_ragna_opening_action_000_003": "ragna_hmph",
        "wg2_tutorial_trigger_ragna_opening_action_002_003": "ragna_laugh3",
        "wg2_tutorial_trigger_used_groove_conclusion_action_005_003": "ragna_getgood",
    },
}


def main() -> None:
    draft = json.loads(DRAFT.read_text(encoding="utf-8"))["ko-KR"]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    merged: dict[str, str] = {}
    count = 0
    for source in sorted(SOURCE.glob("*.json")):
        resource = json.loads(source.read_text(encoding="utf-8"))
        language = resource["ko-KR"]
        resource_name = source.stem.removeprefix("ko-KR")
        additions = MISSING_ADDITIONS.get(resource_name, {})
        overlap = set(additions) & set(language)
        if overlap:
            raise ValueError(f"missing-key additions already exist: {sorted(overlap)}")
        language.update(additions)
        changed = 0
        for key, value in draft.items():
            if key in language and language[key] != value:
                language[key] = value
                changed += 1
        merged.update(language)
        relative = source.relative_to(SOURCE).with_suffix("")
        json_path = OUTPUT / relative.with_suffix(".json")
        bin_path = OUTPUT / relative.with_suffix(".bin")
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(
            json.dumps(resource, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        bin_path.write_bytes(encode_payload(resource))
        count += changed
    verified_path = WORK / "verified-ko-KR.json"
    verified_path.write_text(
        json.dumps({"ko-KR": merged}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Generated {len(list(SOURCE.glob('*.json')))} resources; "
        f"changed {count} terms; verified strings {len(merged)} keys"
    )


if __name__ == "__main__":
    main()
