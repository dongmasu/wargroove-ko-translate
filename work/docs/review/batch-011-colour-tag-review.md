# Translation Batch 011: Colour Tag Review

Date: 2026-09-27

## Scope

This is a read-only reviewer pass over the colour-related markup candidates
left by the translation coverage audit. No translation resource was modified.

The earlier review plan described 47 colour-tag candidates. Re-running the
comparison against the current work tree produces 25 remaining candidates.
The difference is recorded here rather than silently treating the historical
count as current.

Comparison inputs:

- Windows Wargroove 2 English resources under `src/`;
- current generated Korean resources under `work/`;
- Windows WG2 `art/colours.json`;
- Japanese and Chinese resources available for follow-up context checks.

## Colour Definitions

The Windows WG2 colour table defines the following equivalent pairs:

| Token | Hex |
| --- | --- |
| `black` | `#503b5e` |
| `player_black` | `#503b5e` |
| `blue` | `#335eb0` |
| `player_blue` | `#335eb0` |
| `red` | `#AA003F` |
| `player_red` | `#AA003F` |
| `purple` | `#8013c7` |
| `player_purple` | `#8013c7` |
| `yellow` | `#c57d00` |
| `player_yellow` | `#c57d00` |
| `green` | `#77aa08` |
| `player_green` | `#77aa08` |

Therefore, a difference between a base colour and its `player_*` alias does
not currently change the rendered colour. The `[colour:...]` tags are also
used as explicit state changes: an added `black` or `player_black` tag can
close a highlighted span and prevent colour leakage into following text.

## Findings

### No edit: explicit closing/reset tags

The following 23 Korean values add `[colour:black]` or
`[colour:player_black]` after the highlighted Korean phrase while English
leaves the colour state open at the end of the sentence or uses an implicit
boundary:

- `campaign_final/wg2_f3_high_noon_cutscene_f2_tenri_exposition_dialog_121_text`
- `campaign_final/wg2_f3_high_noon_trigger_tenri_vs_valder_action_000_002`
- `conquest/wg2_alchemist_trigger_event_intro_action_001_002a`
- `conquest/wg2_alchemist_trigger_talk_to_npc_action_000_002`
- `conquest/wg2_heal_event_trigger_heal_event_action_000_002a`
- `conquest/wg2_heal_event_trigger_heal_event_action_000_002c`
- `conquest/wg2_heal_event_trigger_heal_event_action_000_002d`
- `conquest/wg2_lone_settlement_trigger_all_villagers_survived_action_000_002`
- `conquest/wg2_lone_settlement_trigger_guards_prompt_action_003_002`
- `conquest/wg2_lone_settlement_trigger_mystery_event_player_has_enough_gold_action_001_002`
- `conquest/wg2_lone_settlement_trigger_support_choice_action_000_002a`
- `conquest/wg2_merchant_event_trigger_merchant_event_action_000_002`
- `conquest/wg2_merchant_event_trigger_merchant_event_action_002_002b`
- `conquest/wg2_merchant_event_trigger_merchant_event_action_002_002h`
- `conquest/wg2_merchant_event_trigger_training_camp_event_action_000_002`
- `conquest/wg2_merchant_event_trigger_training_camp_event_action_001_002b`
- `conquest/wg2_secret_tower_trigger_warning_action_003_002`
- `conquest/wg2_the_castle_cutscene_victory_elodie_dialog_013_text`
- `conquest/wg2_the_heros_blessing_trigger_mercival_postco_end_action_000_002`
- `conquest/wg2_toll_station_trigger_gold_toll_event_action_000_002`
- `conquest/wg2_toll_station_trigger_gold_toll_event_action_001_002`
- `conquest/wg2_toll_station_trigger_gold_toll_event_action_002_002`
- `campaign_tutorial/wg2_tutorial_trigger_groove_action_001_002`

These are semantically safe under the current colour table. Removing the
closing tags would make the Korean markup less explicit and could affect
subsequent text if the engine carries colour state across a dialogue payload.
Status: `문제 없음`.

### No edit: equivalent player colour alias

This tutorial key replaces the English closing token `[colour:black]` with
`[colour:player_black]`:

- `campaign_tutorial/wg2_tut_3_an_ancient_artefact_trigger_5_player_swordsman_captures_village_action_000_002a`

Both tokens resolve to `#503b5e`, and the opening `[colour:player_1]` and
following `[colour:player_1]` are preserved. No semantic or rendering
difference is present. Status: `문제 없음`.

### Defer: missing closing tag at sentence boundary

One Korean value omits the English closing `[colour:black]`:

- `campaign_air/wg2_a2m1_the_dead_of_night_cutscene_a2m1_scene_2_ragna_takes_gauntlet_dialog_061_text`

English highlights “succeed me as Felheim's ruler” and then continues with
“without sufficient dedication”. Korean moves the highlighted phrase to the
end of the sentence:

- English: `[colour:blue]succeed me as Felheim's ruler[colour:black]` ...
- Korean: `... [colour:blue]펠하임의 통치자로서 나를 잇겠느냐?`

Because the highlighted Korean phrase is sentence-final, the missing reset is
not visibly harmful in this payload. Runtime confirmation is still preferable
before adding a tag, because the translation intentionally changes sentence
structure and no edit is approved by this report. Status: `계속 보류`.

## Decision

No colour-tag translation edit is approved by this batch.

- 24 candidates are `문제 없음`.
- 1 candidate remains `계속 보류` for runtime boundary confirmation.
- No actual colour-definition mismatch was found.
- The historical 47-candidate count should not be used as the current edit
  scope; the reproducible current scope is 25.

The next review target is the remaining delivery-tag differences and then the
large set of English/Korean-identical values after technical identifiers and
intentional values are excluded.
