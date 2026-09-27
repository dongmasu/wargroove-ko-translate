# Translation Batch 008: Markup and Token Review

Date: 2026-09-27

## Scope

This is a read-only reviewer pass over the markup and token differences
identified by the translation coverage audit. No translation resource was
modified.

The audit reports 310 token-set differences. A separate order-sensitive scan
also found 67 keys whose token sets match but whose token order differs.

## Candidate Classes

| Candidate | Count | Review meaning |
| --- | ---: | --- |
| Token-set differences | 310 | A token was added, removed, or changed |
| Format-token order changes | 59 | `{0}`, `{1}`, etc. appear in a different Korean order |
| Numeric display-token order changes | 2 | `[0]` and `[1]` appear in a different Korean order |
| Delivery/markup order changes | 6 | Effect tags move with the translated phrase |

The existing automated checks correctly reject token count mismatches, but
they intentionally allow reordering because Korean syntax may require a
different display order. Reordering therefore requires semantic or runtime
review rather than an automatic edit.

## Confirmed Review Targets

### Numeric display tokens

These two keys require in-game substitution confirmation:

- `wg2_e1m3_a_door_in_the_forest_trigger_lytra_progress_count_action_000_000`
- `wg2_s1m3_saffron_riot_trigger_turn_countdown_constant_objective_action_000_000`

Both Korean strings place the total-turn token before the current-turn token,
which is natural Korean but differs from the source order. The expected
display must be checked with known values such as current `2`, total `5`.

### Format-token order

The 59 `{n}` reorderings are concentrated in trigger-action and
trigger-condition readable labels under the root, `wargroove2`, and
`wargroove2_dev` resources. They are likely deliberate parameter-order
changes for Korean UI grammar, but each label must be checked against the
corresponding action/condition field order before approval.

Exact keys:

- `trigger_action_readable_add_ui_tutorial`
- `trigger_action_readable_ai_set_restriction`
- `trigger_action_readable_change_unit_type`
- `trigger_action_readable_convert`
- `trigger_action_readable_count_units`
- `trigger_action_readable_location_boolean_operation`
- `trigger_action_readable_modify_counter`
- `trigger_action_readable_modify_gold`
- `trigger_action_readable_modify_groove`
- `trigger_action_readable_modify_health`
- `trigger_action_readable_move_location_to_unit`
- `trigger_action_readable_play_sound_effect`
- `trigger_action_readable_set_conditional_location_highlight`
- `trigger_action_readable_set_damage_taken`
- `trigger_action_readable_set_location_highlight`
- `trigger_action_readable_set_unit_spent`
- `trigger_action_readable_set_weather`
- `trigger_action_readable_transfer_gizmo_state`
- `trigger_action_readable_transfer_gold`
- `trigger_action_readable_transfer_groove`
- `trigger_action_readable_transfer_health`
- `trigger_action_readable_unit_teleport`
- `trigger_condition_readable_check_gizmo_state`
- `trigger_condition_readable_counter_compare`
- `trigger_condition_readable_unit_groove`
- `trigger_condition_readable_unit_health`
- `trigger_condition_readable_unit_killed`
- `trigger_condition_readable_unit_lost`
- `trigger_condition_readable_unit_presence`
- `trigger_action_readable_activate_flood`
- `trigger_action_readable_conditional_skip_actions`
- `trigger_action_readable_drop_unit`
- `trigger_action_readable_execute_blessing`
- `trigger_action_readable_fade_stage`
- `trigger_action_readable_pick_blessing`
- `trigger_action_readable_play_character_introduction`
- `trigger_action_readable_play_shout`
- `trigger_action_readable_remove_units`
- `trigger_action_readable_reveal_fow`
- `trigger_action_readable_set_map_music`
- `trigger_action_readable_set_protagonist`
- `trigger_action_readable_spawn_animation`
- `trigger_action_readable_spawn_item`
- `trigger_action_readable_spawn_unit`
- `trigger_action_readable_spawn_unit_inside`
- `trigger_action_readable_unit_action`
- `trigger_action_readable_unit_faction_override`
- `trigger_condition_readable_item_presence`
- `trigger_condition_readable_unit_ambushed`
- `trigger_condition_readable_unit_groove_tiered`
- `trigger_condition_readable_unit_groove_verb_used`
- `trigger_condition_readable_unit_interactions_used`
- `trigger_condition_readable_unit_item_presence`
- `trigger_condition_readable_unit_verb_used`
- `trigger_condition_readable_unit_visible`
- `trigger_action_readable_force_action`
- `trigger_action_readable_force_open_ui_tutorial`
- `trigger_action_readable_queue_force_action`
- `trigger_action_readable_queue_force_open_ui_tutorial`

No format-token order change is approved for editing by this report.

### Delivery tags

Campaign dialogue commonly moves `[wavy]`, `[shaking]`, `[slow]`, or
`[short_pause]` around the translated phrase. This can be correct when the
highlighted word moves in Korean, but it can also change timing or emphasis.
Review must compare:

- the highlighted Korean phrase with the highlighted English phrase;
- whether opening/closing effect tags remain balanced for the game parser;
- whether `[instant]`, pause, and speed tags still occur at the same intended
  dialogue boundary.

### Colour tags

Several Korean strings add explicit `[colour:black]` or use
`[colour:player_black]` where English uses a different closing or player
colour token. These are not approved for bulk normalization. The reviewer
must verify the target UI colour scheme before changing them.

### `ui_cutscene` labels

The 70 `ui_cutscene` differences mostly translate labels such as `[Bark 2]`,
`[Pain 3]`, and `[Ghostly]` into Korean bracket labels. These are display
labels and should not be treated as gameplay markup without runtime evidence.
They remain a low-priority consistency review, not an automatic correction.

## Current Decision

No confirmed translation or markup edit is approved by this batch. The next
reviewer work should close the two numeric-token keys and sample the 59
format-token reorderings by resource family. The editor must wait for an
approver-approved key list.
