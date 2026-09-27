# Translation Batch 015: Campaign Air A1M1/A1M2 Tutorial Review

Date: 2026-09-27

## Scope

This is a read-only review of player-facing tutorial prompts, unit guidance,
and bonus objectives in Campaign Air missions A1M1 and A1M2. The review
checks whether the Korean text gives the same gameplay instruction as English
and uses the established unit terminology.

No translation resource was modified.

## Proposed Changes

### A1M1-003: natural phrase for air-unit targeting

- Key:
  `wg2_a1m1_cry_for_help_trigger_player_turn_1_action_000_002`
- English: `Most Land-based units are incapable of attacking units in the Air.`
- Current Korean:
  `대부분의 지상 유닛은 공중의 유닛을 공격하지 못한다.`
- Proposed Korean:
  `대부분의 지상 유닛은 공중 유닛을 공격하지 못한다.`
- Issue: naturalness and terminology consistency
- Reason: The current `공중의 유닛` is grammatically understandable but
  unnatural. The same tutorial block and the glossary consistently use
  `공중 유닛`.
- Status: `수정`
- Confidence: high

### A1M1-004: natural phrase for Archer effectiveness

- Key:
  `wg2_a1m1_cry_for_help_trigger_player_turn_1_action_001_002a`
- English: `Archers aren't the best at countering Air units, but they'll work in a pinch.`
- Current Korean:
  `궁수가 공중 유닛 상대로 [wavy]최선[wavy]은 아니지만, 급할 때는 제 몫을 합니다.`
- Proposed Korean:
  `궁수는 공중 유닛을 상대하는 데 [wavy]최선[wavy]은 아니지만, 급할 때는 제 몫을 합니다.`
- Issue: naturalness
- Reason: `궁수가 ... 최선은` uses an awkward subject-predicate construction.
  The proposed sentence preserves the gameplay meaning and the effect tag.
- Status: `수정`
- Confidence: high

### A1M2-001: tower recruitment instruction

- Key:
  `wg2_a1m2_felheim_in_fallow_trigger_review_tower_option_action_001_002`
- English: `This Tower only supplies Aeronauts, but you'll discover more types later.`
- Japanese: `この塔では飛行隊しか雇用できませんが、ゲームを進めると雇用できるユニットの種類が増えていきます。`
- Current Korean:
  `이 탑은 [colour:player_1]스카이어태커만[colour:black] 공급하지만, 나중에 더 많은 종류를 만나게 됩니다.`
- Proposed Korean:
  `이 탑에서는 [colour:player_1]스카이어태커만[colour:black] 모집할 수 있지만, 나중에 다른 종류의 유닛도 만나게 됩니다.`
- Issue: tutorial naturalness and action terminology
- Reason: A tower recruits units; it does not “supply” them. The current
  wording also leaves `more types` without an explicit unit referent.
- Status: `수정`
- Confidence: high

## Deferred Findings

### A1M2 bonus objective: `seasoned hunters`

- Key: `wg2_campaign_a1m2_felheim_in_fallow_bonus_objective_0`
- English: `Defeat Oddvar using a pair of seasoned hunters.`
- Current Korean: `노련한 사냥꾼 한 쌍으로 오드바르를 물리치기`
- Japanese: `狩猟犬２匹を使ってオドヴァルを倒す。`

English suggests two experienced hunters, while Japanese literally indicates
two hunting dogs. The current Korean follows the English but may be wrong if
the objective refers to a specific pair of dog units. The actual A1M2 unit
roster and objective trigger must be checked before proposing either
`노련한 사냥꾼` or `사냥개`. Status: `계속 보류`.

### A1M1 map objective specificity

- Key: `wg2_campaign_mapobjective_a1m1_cry_for_help`
- English: `Go back to the Castle.`
- Current Korean: `성으로 돌아가라.`
- Japanese: `チェリーストーン城に戻ろう。`
- Possible Korean: `체리스톤 성으로 돌아가라.`

The current wording is natural but less specific than the Japanese reference
and the known map context. Keep deferred until the campaign objective is
checked in the map UI, where shorter wording may be intentional. Status:
`계속 보류`.

## No Edit

The following items were checked and do not require a wording change:

- `wg2_a1m1_cry_for_help_trigger_player_turn_1_action_000_002a`
  - `궁수는 몇 안 되는 예외입니다` correctly communicates the exception.
- `wg2_a1m2_felheim_in_fallow_trigger_review_tower_option_action_000_002`
  - `탑에서는 공중 유닛을 모집할 수 있습니다` is concise and accurate.
- `wg2_campaign_a1m2_felheim_in_fallow_bonus_objective_1`
  - `제재소를 모두 점거하기` matches the established `제재소` terminology.
- `wg2_a1m2_felheim_in_fallow_trigger_objective_defeat_oddvar_action_000_000`
  - `오드바르를 물리쳐라` is a correct objective-style rendering.

Status for these items: `문제 없음`.

## Decision

- Proposed editor changes: 3 keys.
- Deferred runtime/context findings: 2 keys.
- No-edit findings: 4 keys.
- No translation resource was modified.
- The three proposed changes require approver approval before editing.

The next review scope is the remaining A1M2 campaign dialogue and objectives,
followed by A1M3 tutorial text. The `seasoned hunters` objective should be
resolved through the actual stage unit roster before approval.
