# Translation Batch 023: Campaign Air A2M3 Review

Date: 2026-09-27

## Scope

This is a read-only review of Campaign Air A2M3, including the crash-site
exploration, item interactions, bridge instructions, and the fireplace
conversation. The mission's map title, description, and objective are
intentional placeholder ellipses in the source and are treated separately.

No translation resource was modified.

## Proposed Changes

### A2M3-001: movement objective wording

- Key: `wg2_a2m3_trigger_all_items_get_action_006_000`
- English: `Make your way to the old house.`
- Current Korean: `낡은 집까지 나아가라.`
- Proposed Korean: `낡은 집으로 가라.`
- Issue: objective naturalness
- Reason: `나아가다` is unnatural in this short navigation objective and can
  suggest advancing abstractly rather than moving to a location. `-으로
  가라` is the established concise objective style.
- Status: `수정`
- Confidence: high

### A2M3-002: bridge gap explanation

- Key: `wg2_a2m3_trigger_bridge_1_action_001_002`
- English: `The gap here's small enough...`
- Japanese: `川幅はそんなにないね…`
- Current Korean: `여기 틈이 좁아...`
- Proposed Korean: `여기 틈은 충분히 좁으니까...`
- Issue: meaning and naturalness
- Reason: The source establishes that the gap is narrow enough for the next
  bridge-plank solution. The current sentence only states that it is narrow
  and sounds incomplete; `충분히` supplies the intended causal setup.
- Status: `수정`
- Confidence: medium

## No Edit

The following sampled strings were checked and require no wording change:

- `wg2_a2m3_trigger_bridge_1_action_002_002`
  - `저 나무판자로 건널 수 있을 것 같은데!` correctly introduces the bridge
    solution.
- `wg2_a2m3_trigger_fissure_exploration_action_004_002`
  - `거대 광폭 펠뱃 둥지!` correctly conveys the discovered enemy nest and
    preserves the item colour and wavy tags.
- `wg2_a2m3_trigger_item_2_get_sparrow_bomb_action_001_002`
  - `코지가 만든 [wavy]'펑' 하는 새잖아!` naturally explains the Sparrow
    Bomb in character voice.
- `wg2_a2m3_trigger_item_3_get_gold_action_002_002`
  - `태어나서 ... 처음 봐!` correctly preserves the exaggerated lifetime
    emphasis.
- `wg2_a2m3_cutscene_fireplace_dialog_009_text`
  - `내가 그만하라고 [shaking]말했는데도!` accurately keeps the stressed
    interruption.
- `wg2_a2m3_cutscene_fireplace_dialog_040_text`
  - `여기서 둘 다 얼어 죽으면 말은 [wavy]꺼내지도 못하잖아!` is a natural
    adaptation of the inability to talk to Koji.
- `wg2_a2m3_trigger_trail_4_action_001_002`
  - The month-long silence is conveyed clearly and the wavy tag is retained.
- `wg2_a2m3_trigger_trail_6_action_001_002`
  - The stammered apology and sibling relationship are preserved.

Status for these items: `문제 없음`.

## Internal/Developer Text and Placeholders

The following are intentionally internal or source placeholders:

- `SFX here`
- `DEVNOTE: THIS IS A PLACEHOLDER FOR A LORE UNLOCK`
- The weather-audio implementation note
- A2M3 map description, map name, region, and map objective represented by
  ellipses

They require no translation wording change in this review.

## Decision

- Proposed editor changes: 2 keys.
- No-edit findings: 8 sampled keys.
- Internal/placeholder findings: no change.
- No translation resource was modified.
- The two proposed changes require approver approval before editing.

The next review scope is Campaign Air A2M4.
