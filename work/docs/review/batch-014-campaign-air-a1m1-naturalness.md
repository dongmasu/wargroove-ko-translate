# Translation Batch 014: Campaign Air A1M1 Residual Naturalness

Date: 2026-09-27

## Scope

This is a read-only follow-up to Batch 003. It covers the remaining
`campaign_air` A1M1 dialogue, tutorial prompts, objectives, and map labels
after the six opening-dialogue corrections already recorded in Batch 003.

Evidence priority:

1. Windows WG2 English;
2. Japanese and Simplified Chinese references;
3. current Korean wording and campaign context.

No translation resource was modified.

## Proposed Changes

### A1M1-001: `duties` meaning

- Key:
  `wg2_a1m1_cry_for_help_cutscene_a1m1_scene_1_intro_dialog_036_text`
- English: `Prince Koji. Your [shaking]duties.`
- Japanese: `コージ様。[shaking]公務中[shaking]ですぞ。`
- Current Korean: `코지 왕자님. [shaking]본분을 잊지 마십시오.`
- Proposed Korean: `코지 왕자님. [shaking]공무 중이십니다.`
- Issue: meaning/context
- Reason: English and Japanese refer to Koji being on official duty. The
  current Korean changes this into a general admonition to remember his
  responsibilities.
- Status: `수정`
- Confidence: high

### A1M1-002: omitted object in `gobbled 'em up`

- Key:
  `wg2_a1m1_cry_for_help_trigger_player_turn_4_cherrystone_interlude_action_001_002`
- English: `Maybe the skellies already [shaking]gobbled[shaking] 'em up!`
- Japanese: `ガイコツたちに全員[shaking]食べられちゃった[shaking]のかも！`
- Current Korean: `해골들이 벌써 [shaking]꿀꺽[shaking] 했을지도 모르지!`
- Proposed Korean: `해골들이 벌써 [shaking]다 먹어 치웠을지도 모르지!`
- Issue: meaning/naturalness
- Reason: `꿀꺽` is an adverbial sound expression and has no natural object
  or verb in the current sentence. The source and Japanese explicitly mean
  that the guards were all eaten.
- Status: `수정`
- Confidence: high

## No Edit

The following A1M1 items were checked as natural or contextually acceptable:

- `wg2_a1m1_cry_for_help_cutscene_a1m1_scene_1_intro_dialog_117_text`
  - `Pray, let me be your blade!` -> `부디, 내가 그대의 칼이 되게 하라!`
  - The archaic Korean register appropriately follows the source speaker.
- `wg2_a1m1_cry_for_help_cutscene_a1m1_scene_1_intro_dialog_125_text`
  - `One night, Prince Koji.` -> `하룻밤입니다, 왕자님.`
  - Concise and consistent with the Japanese reference.
- `wg2_a1m1_cry_for_help_trigger_player_turn_3_be_brave_errol_action_002_002`
  - `I can do both!` -> `둘 다 할 수 있어!`
  - Correctly preserves the joke established by the preceding line.
- `wg2_a1m1_cry_for_help_trigger_opening_cutscene_action_004_002`
  - `This is just what Felheim does!` -> `펠하임은 원래 이런 놈들입니다!`
  - The added `놈들` is a natural Korean realization of the hostile speaker
    context and does not change the faction reference.

Status for these items: `문제 없음`.

## Defer

### Map-region label

- Key: `wg2_campaign_mapname_a1m1_cry_for_help_region`
- English: `Cherrystone Castle Grounds`
- Current Korean: `체리스톤 성 앞뜰`
- Japanese: `チェリーストーン城の敷地`

`앞뜰` is narrower than the source's castle grounds, but it may match the
actual map area and is concise for the campaign-selection UI. Keep as
`계속 보류` until the map-selection screen is checked in Windows. No edit is
approved from text comparison alone.

### Internal placeholder prompts

The following A1M1 strings are developer or future-feature prompts rather than
player-facing narrative:

- `wg2_a1m1_cry_for_help_trigger_placeholder_losing_too_many_archers_action_000_002`
- `wg2_a1m1_cry_for_help_trigger_secret_1_action_000_002`
- `wg2_a1m1_cry_for_help_trigger_secret_1_action_001_002`
- `wg2_a1m1_cry_for_help_trigger_secret_2_action_000_002`
- `wg2_a1m1_cry_for_help_trigger_secret_2_action_001_002`

The existing Korean is understandable as internal text. Their runtime
visibility and intended final wording are unknown. Status: `계속 보류`.

## Decision

- Proposed editor changes: 2 keys.
- Naturalness issues confirmed with source/reference evidence: 2.
- No-edit findings: 4 sampled keys.
- Runtime/UI deferrals: 6 keys.
- No translation resource was changed.
- The two proposed changes require approver approval before editing.

The next review scope is A1M1/A1M2 campaign-air objectives and tutorial
instructions, with particular attention to faction/unit terminology and
player-facing map objectives.
