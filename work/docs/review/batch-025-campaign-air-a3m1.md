# Translation Batch 025: Campaign Air A3M1 Review

Date: 2026-09-27

## Scope

This is a read-only review of Campaign Air A3M1, `Bottom of the World`,
covering the southern-arrival cutscene, Prince Harmon objective, bonus
objectives, and map metadata.

No translation resource was modified.

## Proposed Changes

### A3M1-001: map-description wordplay

- Key: `wg2_campaign_mapdescription_a3m1_bottom_of_the_world`
- English: `Things head south. People, too.`
- Japanese: `事態は悪化の一途をたどる。`
- Current Korean: `상황이 남쪽으로 향한다. 사람들도.`
- Proposed Korean: `상황은 점점 악화되고, 사람들도 남쪽으로 향한다.`
- Issue: literal translation and naturalness
- Reason: The current Korean does not form a natural sentence and makes
  `상황이 남쪽으로 향한다` sound spatial rather than idiomatic. The
  proposed wording conveys both halves of the source joke: circumstances
  worsen, while the people physically head south.
- Status: `수정`
- Confidence: high

## No Edit

The following sampled strings were checked and require no wording change:

- `wg2_a3m1_bottom_of_the_world_trigger_mission_objective_action_000_000`
  - `캐코포니의 왕자를 물리쳐라.` correctly renders the named enemy.
- `wg2_campaign_a3m1_bottom_of_the_world_bonus_objective_0`
  - `발더로 하몬 왕자를 물리치기` clearly states the required commander.
- `wg2_campaign_a3m1_bottom_of_the_world_bonus_objective_1`
  - `새 유닛을 5기 넘게 모집하지 않고 승리하기` correctly expresses the
    recruitment limit.
- `wg2_campaign_mapobjective_a3m1_bottom_of_the_world`
  - `라그나에게 가서 펠 건틀릿을 되찾아라.` is a clear two-part objective.
- `wg2_a3m1_bottom_of_the_world_cutscene_air_campaign_act_3_map_1_intro_dialog_017_text`
  - The army warning and shaking emphasis are naturally preserved.
- `wg2_a3m1_bottom_of_the_world_cutscene_air_campaign_act_3_map_1_intro_dialog_019_text`
  - `아무것도 건드리지 말고` correctly carries the imperative and emphasis.
- `wg2_a3m1_bottom_of_the_world_trigger_player_turn_4_action_001_002`
  - `너는 나를 망신시켰다` accurately preserves the quoted accusation.
- `wg2_a3m1_bottom_of_the_world_trigger_player_turn_7_action_001_002`
  - `그저 돌아오기만 해라!` correctly preserves the urgent emotional appeal.
- `wg2_a3m1_bottom_of_the_world_trigger_ragna_attacks_valder_action_002_002`
  - `그 아이가 무척 실망스럽겠군` is a natural rendering of disappointment.

Status for these items: `문제 없음`.

## Decision

- Proposed editor changes: 1 key.
- No-edit findings: 9 sampled keys.
- No translation resource was modified.
- The proposed change requires approver approval before editing.

The next review scope is the final Campaign Air mission, A3M2.
