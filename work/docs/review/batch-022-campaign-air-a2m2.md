# Translation Batch 022: Campaign Air A2M2 Review

Date: 2026-09-27

## Scope

This is a read-only review of Campaign Air A2M2, `The Guardian`, covering
the mission objective, Guardian dialogue, and campaign map metadata. The
review compares English with Japanese and Simplified Chinese references.

No translation resource was modified.

## Proposed Changes

### A2M2-001: `Not-Ragna` map description

- Key: `wg2_campaign_mapdescription_a2m2_the_guardian`
- English: `Vesper and Not-Ragna make an ancient discovery near the South Pole.`
- Japanese:
  `ヴェスパーとラグナを操る者は、南極付近で古代遺跡を発見する。`
- Current Korean:
  `베스퍼와 라그나 아닌 라그나가 남극 근처에서 고대의 유물을 발견한다.`
- Proposed Korean:
  `베스퍼와 가짜 라그나가 남극 근처에서 고대 유적을 발견한다.`
- Issue: literal translation and naturalness
- Reason: `라그나 아닌 라그나` is not natural Korean and obscures that the
  second character is a false/doppelganger version of Ragna. The references
  also describe an ancient ruin rather than a portable relic. The proposed
  sentence is concise and preserves both distinctions.
- Status: `수정`
- Confidence: high

## No Edit

The following sampled strings were checked and require no wording change:

- `wg2_campaign_a2m2_the_guardian_bonus_objective_0`
  - `수호자를 물리치지 않고 승리하기` correctly expresses the restriction.
- `wg2_campaign_a2m2_the_guardian_bonus_objective_1`
  - `같은 턴에 적 사령관 둘을 모두 물리치기` is clear and objective-style.
- `wg2_a2m2_the_guardian_trigger_mission_objective_action_000_000`
  - `앞을 가로막는 자들을 물리쳐라.` accurately conveys the mission goal.
- `wg2_a2m2_the_guardian_trigger_guardian_turn_1_action_000_002`
  - `저 수호자를 우리 것으로 삼는 게 좋겠다.` naturally conveys making use
    of the Guardian.
- `wg2_a2m2_the_guardian_trigger_opening_cutscene_villagers_action_004_002`
  - `수호자를 깨우겠어` correctly renders activating/awakening the Guardian.
- `wg2_a2m2_the_guardian_trigger_player_captures_guardian_action_000_002`
  - `굳건한 수호자여` and the kingdom colour tags are preserved correctly.
- `wg2_a2m2_the_guardian_trigger_p2_turn_3_errols_cold_action_005_002`
  - `라그나를 막고 [shaking]나서!` preserves the timing emphasis.
- `wg2_a2m2_the_guardian_trigger_win_twins_koji_are_dead_action_000_002`
  - `다들! [shaking]당장[shaking] 배로 돌아가!!` is an accurate urgent
    retreat instruction.

Status for these items: `문제 없음`.

## Decision

- Proposed editor changes: 1 key.
- No-edit findings: 8 sampled keys.
- No translation resource was modified.
- The proposed change requires approver approval before editing.

The next review scope is Campaign Air A2M3.
