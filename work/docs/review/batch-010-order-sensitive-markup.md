# Translation Batch 010: Order-Sensitive Markup Findings

Date: 2026-09-27

## Scope

Eight candidates whose markup token order differs while the token multiset is
unchanged were reviewed against the English sentence and Korean phrase order.
No translation resource was modified.

## Results

### Natural Korean reordering: no edit

The following six keys move emphasis or colour tags with the phrase that is
emphasized in Korean. The meaning and token identity are preserved:

- `wg2_a1m2_felheim_in_fallow_trigger_win_defeat_oddvar_action_001_002`
- `wg2_e2m1_her_loyal_assistant_trigger_lytra_has_0_units_left_action_004_002`
- `wg2_f1_that_awful_night_cutscene_f1_scene_1_emeric_and_mercival_dialog_051_text`
- `wg2_f4_a_voice_from_beyond_trigger_player_turn_1_action_001_002`
- `wg2_s1m1_highseas_robbery_cutscene_s1m1_scene_2_the_queens_request_dialog_073_text`
- `wg2_lone_settlement_trigger_mystery_event_player_has_enough_gold_action_003_002`

Status: `문제 없음` for token ordering. They remain subject to general
naturalness review.

### Numeric display-token order: runtime confirmation

These two keys use `[1]` before `[0]` in Korean to show total turns before the
current turn:

- `wg2_e1m3_a_door_in_the_forest_trigger_lytra_progress_count_action_000_000`
- `wg2_s1m3_saffron_riot_trigger_turn_countdown_constant_objective_action_000_000`

Status: `계속 보류`

The intended display should be checked with known values, for example current
turn `2` and total turns `5`. If the result displays as `5턴 중 2턴`, the
reordering is correct. If the game substitutes by position rather than token
identity, the strings require revision.

## Decision

No additional translation edit is approved by this batch. The six textual
reorderings are accepted as intentional, and the two numeric-token keys remain
runtime verification targets.
