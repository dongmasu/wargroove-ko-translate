# Translation Batch 026: Campaign Air A3M2 Review

Date: 2026-09-27

## Scope

This is the final resource-level review of Campaign Air A3M2, including the
Portal tutorial, final campaign dialogue, objectives, bonus objectives, and
the known corrupted-looking source strings.

No translation resource was modified.

## Proposed Changes

### A3M2-001: bird objective wording

- Key: `wg2_campaign_a3m2_¤ΐж※Ħ※×§_bonus_objective_1`
- English: `Defeat the enemy Commander with a bird.`
- Japanese: `鳥で敵司令官を倒す。`
- Current Korean: `새로 적 사령관을 물리치기`
- Proposed Korean: `새를 이용해 적 사령관을 물리치기`
- Issue: omitted particle and incorrect spacing/meaning
- Reason: The current text reads as if `새로` means “newly,” and it does not
  express that a bird must be used to defeat the Commander. The proposed
  wording explicitly preserves the required method.
- Status: `수정`
- Confidence: high

## No Edit

The following sampled strings were checked and require no wording change:

- `wg2_a3m2_¤ΐж※Ħ※×§_trigger_objective_update_action_000_000`
  - `실모어의 소르디노 왕자를 물리쳐라!` correctly renders the named
    Commander objective.
- `wg2_a3m2_¤ΐж※Ħ※×§_trigger_portal_tutorial_action_000_002a`
  - `차원문이 둘 이상이면 유닛이 그 사이를 순간이동할 수 있습니다.` clearly
    explains the Portal mechanic.
- `wg2_campaign_a3m2_¤ΐж※Ħ※×§_bonus_objective_0`
  - `12턴 이내에 승리하기` is a correct turn-limit objective.
- `wg2_campaign_mapname_a3m2_¤ΐж※Ħ※×§_region`
  - `침묵의 신전` correctly matches `Temple of Silence`.
- `wg2_a3m2_¤ΐж※Ħ※×§_cutscene_a3m2_scene_2_gauntlets_leave_dialog_006_text`
  - `몸이 없는 삶이란 [wavy]참혹하더군요!` accurately conveys the
    harrowing-bodyless-life line.
- `wg2_a3m2_¤ΐж※Ħ※×§_trigger_koji_3_player_destroys_a_second_growth_action_006_002`
  - `난 [shaking]왕자야.` correctly preserves Koji's self-assertion.
- `wg2_a3m2_¤ΐж※Ħ※×§_trigger_sordino_awakens_action_005_002`
  - `피도 눈물도 없는 마귀할멈` is a natural hostile rendering.
- `wg2_a3m2_¤ΐж※Ħ※×§_cutscene_a3m2_scene_3_much_needed_rest_narration_114_text`
  - `[하늘 캠페인 종료]` correctly localizes the end-of-campaign marker.

Status for these items: `문제 없음`.

## Deferred Corrupted/Placeholder Strings

The following A3M2 values are not ordinary translatable prose:

- `wg2_campaign_mapdescription_a3m2_¤ΐж※Ħ※×§`
- `wg2_campaign_mapname_a3m2_¤ΐж※Ħ※×§`
- `wg2_a3m2_¤ΐж※Ħ※×§_cutscene_a3m2_scene_1_intro_dialog_070_text`

Their source contains corrupted-looking symbols and the Korean value is
`???`. These were already identified in the P0/missing-resource review.
Without a valid source string or runtime context, they remain deferred and
must not be guessed.

## Decision

- Proposed editor changes: 1 key.
- Deferred corrupted/placeholder findings: 3 keys.
- No-edit findings: 8 sampled keys.
- No translation resource was modified.
- The proposed change requires approver approval before editing.

Campaign Air A1M1 through A3M2 resource-level review is complete.
