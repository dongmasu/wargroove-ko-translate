# Translation Batch 012: Delivery and Effect Tag Review

Date: 2026-09-27

## Scope

This is a read-only review of delivery/effect markup differences in campaign,
tutorial, and Conquest dialogue. UI voice-cue labels such as `[Bark 2]` and
`[Pain 3]` are excluded because they are display labels, not dialogue
delivery controls.

The current comparison finds 203 keys containing differences in one or more
of these tags:

- `[wavy]`
- `[shaking]`
- `[scared]`
- `[slow]`
- `[fast]`
- `[instant]`
- `[short_pause]`
- `[long_pause]`

No translation resource was modified.

## Classification

| Class | Count | Decision |
| --- | ---: | --- |
| Single `wavy`/`shaking`/`scared` count difference, no timing tag | 135 | Natural phrase-boundary movement; no edit |
| Single effect count difference with timing tag present | 58 | Runtime confirmation required |
| Complex or multi-tag difference | 10 | Individual semantic/runtime review required |
| Total | 203 | No bulk edit |

The 135 low-risk cases generally convert an English single effect marker at
the sentence boundary into an explicit Korean opening/closing pair, or omit a
closing marker after moving the emphasized phrase. This follows the same
phrase-localization pattern accepted in Batch 010, but does not authorize
global normalization.

## Timing Candidates

The 58 simple timing-sensitive candidates are part of a larger runtime
confirmation set. Nine of the ten complex candidates also contain timing
tags, so the total runtime-sensitive set is 67 keys. The 67 candidates are
distributed as follows:

| Resource | Count |
| --- | ---: |
| `campaign_sea` | 23 |
| `campaign_air` | 16 |
| `campaign_earth` | 12 |
| `campaign_final` | 10 |
| `conquest` | 6 |

These remain `계속 보류` until Windows runtime confirms that Korean
`[short_pause]`, `[long_pause]`, `[slow]`, `[fast]`, and `[instant]` occur at
the intended dialogue boundary. The reviewer did not infer timing correctness
from token counts alone.

Examples requiring runtime confirmation:

- `campaign_air/wg2_a3m1_bottom_of_the_world_trigger_player_turn_4_action_002_002`
  has two English `[wavy]... [wavy]` spans around separate clauses, while
  Korean retains one span in each clause and preserves `[long_pause]`.
- `campaign_sea/wg2_s2m2_security_trigger_ryota_attacks_wulfar_action_004_002`
  and `campaign_sea/wg2_s2m2_security_trigger_wulfar_attacks_ryota_action_004_002`
  omit one English `[short_pause]` before the `[slow]` delivery.
- `campaign_sea/wg2_s1m1_highseas_robbery_trigger_player_turn_1_end_action_003_002`
  retains `[short_pause]` but removes the English emphasized phrase tags
  around “are”.

These are evidence targets, not approved edits.

## Complex Candidates

The following ten keys cannot be explained by a single phrase-boundary
opening/closing difference:

- `campaign_air/wg2_a3m2_¤ΐж※Ħ※×§_cutscene_a3m2_scene_1_intro_dialog_070_text`
  - English source is corrupted symbol text with many delivery tags; Korean
    is `[wavy][slow]???`. Keep deferred under the existing source-defect
    policy.
- `campaign_air/wg2_a3m1_bottom_of_the_world_trigger_player_turn_4_action_002_002`
  - Two emphasized clauses and a `[long_pause]` require runtime boundary
    confirmation.
- `campaign_earth/wg2_e1m4_forgotten_halls_cutscene_e1m4_scene_3_findings_report_dialog_030_text`
  - English has a pause before the emphasized question; Korean moves the
    emphasis but removes that pause.
- `campaign_sea/wg2_s1m1_highseas_robbery_trigger_player_turn_1_end_action_003_002`
  - English emphasis is omitted while the pause remains.
- `campaign_sea/wg2_s1m3_saffron_riot_cutscene_sea_campaign_act_1_mission_3_extro_dialog_078_text`
  - Korean adds `[short_pause]` before the emphasized phrase.
- `campaign_sea/wg2_s2m2_security_trigger_ryota_attacks_wulfar_action_004_002`
  - One English pause is omitted before `[slow]`.
- `campaign_sea/wg2_s2m2_security_trigger_wulfar_attacks_ryota_action_004_002`
  - Same pause structure as the preceding mirrored line.
- `conquest/wg2_forests_edge_trigger_initial_map_setup_intro_action_001_002`
  - English contains two pauses before the final `[shaking]` delivery; Korean
    contains one.
- `conquest/wg2_forests_edge_trigger_initial_map_setup_intro_vesper_action_000_002`
  - The English source is a French placeholder with character-level effects;
    Korean is a semantic translation and cannot be token-normalized.
- `conquest/wg2_secret_tower_trigger_warning_action_001_002`
  - English applies `[wavy]` to “thrilled” and `[shaking]` to “head”; Korean
    reverses the emphasis order with the translated phrase order.

All ten are `계속 보류`. None is approved for editor changes.

## Decision

- 135 cases are accepted as natural Korean emphasis-boundary movement:
  `문제 없음`.
- 67 timing-sensitive cases remain `계속 보류` for Windows runtime testing
  (58 simple cases plus 9 complex cases).
- 10 complex cases remain `계속 보류` for individual semantic/runtime review.
- No delivery/effect tag edit is approved by this batch.
- The translated `ui_cutscene` voice labels remain a separate low-priority
  display-label review and are not mixed into this decision.

The next review target is the English/Korean-identical value set after
technical identifiers, numbers, labels, and intentional source reuse are
excluded.
