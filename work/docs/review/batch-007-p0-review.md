# Translation Batch 007: P0 Reviewer Findings

Date: 2026-09-27

## Reviewer Scope

Read-only comparison of the P0 candidates from
`batch-007-review-scope.md`. Translation resources were not modified.
References used:

1. Windows Wargroove 2 English, Japanese, Simplified Chinese, and
   Traditional Chinese resources under `src/`;
2. NSW Wargroove 2 `config.dat` decoded read-only from
   `references/posts/WG2_KR/romfs/config.dat`;
3. current Korean resources under `work/`;
4. `translation-exceptions.tsv` and earlier batch reports.

## Findings

### P0-001: Corrupted campaign-air source block

Status: `계속 보류`

The following four keys have damaged source identifiers or source text:

- `wg2_a3m2_¤ΐж※Ħ※×§_cutscene_a3m2_scene_1_intro_dialog_070_text`
- `wg2_a3m2_¤ΐж※Ħ※×§_trigger_player_destroys_growth_1_action_003_002`
- `wg2_campaign_mapdescription_a3m2_¤ΐж※Ħ※×§`
- `wg2_campaign_mapname_a3m2_¤ΐж※Ħ※×§`

English and Japanese contain the same corrupted symbols for all four. Chinese
uses `？？？` for the map name and description, while the NSW Korean resource
has no corresponding key. The first key also contains control tags around
corrupted symbols. There is no reliable linguistic evidence for a Korean
replacement, so the existing `???` values are retained.

### P0-002: Empty Korean values

Status: `문제 없음` for structural retention; no translation edit approved

The 22 empty values are blank English metadata, absent from the corresponding
reference resources, or developer/voice-cue/title fields with no translatable
source:

- `character_elodie_age`
- `character_elodie_birthday`
- `character_elodie_birthplace`
- `character_vesper_birthday`
- `ui_cutscene_shout_nadia_die_ghost`
- `ui_cutscene_shout_nadia_die_no_battle`
- `ui_cutscene_shout_nadia_groove`
- `ui_cutscene_shout_nadia_groove_hit`
- `ui_cutscene_shout_nadia_groove_intro`
- `ui_cutscene_shout_nadia_groove_part1`
- `ui_cutscene_shout_nadia_groove_part2`
- `character_donut_title`
- `character_fenris_title`
- `character_floran_captain_title`
- `character_lytra_flying_title`
- `character_lytra_no_harp_title`
- `character_rhomb_angry_title`
- `character_theWarship_title`
- `character_wulfar_pirate_title`
- `codex_unit_boarding_ship_critical_text`
- `ui_sector_properties_colour_tooltip`
- `ui_sector_properties_name_tooltip`

These values remain deferred pending runtime evidence that the fields are
visible and require text.

### P0-003: Bracket-token order candidate

Status: `계속 보류`

Key:

```text
wg2_e1m3_a_door_in_the_forest_trigger_lytra_progress_count_action_000_000
```

English and all three reference languages use `[0]` before `[1]`:

```text
Lytra's Progress: Turn [0] of [1]
```

The current Korean uses `[1]` before `[0]` to produce a natural total/current
order:

```text
리트라의 진행: [1]턴 중 [0]턴
```

This may be intentional, but the current automated tests do not validate
bracket tokens or their order. It requires an in-game value substitution check
before approval. Do not edit it based on string comparison alone.

## Markup Review Queue

The audit reports 310 markup differences. They are not automatically errors:
many are caused by Korean moving a highlighted phrase, adding an explicit
closing colour tag, or translating developer voice-cue labels. The next
review batch must prioritize:

1. numeric/control tokens such as `[0]`, `[1]`, and `[2]`;
2. colour-tag pairs whose target colour differs from the source;
3. `[instant]`, `[short_pause]`, `[long_pause]`, `[fast]`, `[slow]`,
   `[shaking]`, and `[wavy]` changes in campaign dialogue;
4. translated tags in `ui_cutscene` voice-cue labels.

No bulk edit is approved by this report.

## Approval Boundary

The four corrupted keys and 22 empty values are approved for continued
deferral, not for translation edits. The bracket-token item and the markup
queue require evidence or runtime verification. The editor must not modify
translation resources until the approver accepts an exact key list.
