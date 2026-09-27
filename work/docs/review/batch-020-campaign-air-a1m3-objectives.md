# Translation Batch 020: Campaign Air A1M3 Objectives and Combat Follow-up

Date: 2026-09-27

## Scope

This is a read-only follow-up review of Campaign Air A1M3 objectives, map
text, and repeated combat-trigger dialogue after Batches 018 and 019.
The review checks gameplay meaning, unit terminology, character voice, and
markup preservation.

No translation resource was modified.

## No Edit

The following strings were checked and require no wording change:

- `wg2_campaign_a1m3_the_fortress_bonus_objective_0`
  - `10턴 이내에 승리하기` correctly expresses winning within ten turns.
- `wg2_campaign_a1m3_the_fortress_bonus_objective_1`
  - `쌍둥이로 적 사령관을 물리치기` correctly identifies the Twins as the
    required units.
- `wg2_campaign_mapdescription_a1m3_the_fortress`
  - `구조대가 발더 경을 구하러 달려가지만... 너무 늦은 것일까?` naturally
    conveys the urgency and uncertainty of the map description.
- `wg2_campaign_mapname_a1m3_the_fortress_region`
  - `펠하임 요새` is consistent with the established location terminology.
- `wg2_a1m3_the_fortress_trigger_heavensong_attacks_vesper_before_kids_action_001_002`
  - `벌써 거래에서 밀려난 건가...?` correctly renders being cut out of a
    deal.
- `wg2_a1m3_the_fortress_trigger_koji_attacks_vesper_action_001_002`
  - `이게 바로 텐코 Mk. IV야!` preserves the established Tenko name and
    model designation.
- `wg2_a1m3_the_fortress_trigger_vesper_attacks_twins_action_001_002`
  - The insult and `[wavy]` emphasis are both preserved naturally.
- `wg2_a1m3_the_fortress_trigger_vesper_goes_to_sidewings_action_001_002`
  - `어딜 도망쳐, 마귀할멈!` is an appropriate hostile rendering of `hag`.
- `wg2_a1m3_the_fortress_trigger_win_defeat_vesper_boss_action_000_002`
  - `다들! 쫓아가자!` is a concise and correct pursuit callout.

Status for these items: `문제 없음`.

## Deferred Findings

### `renard` unit terminology

- Key:
  `wg2_a1m3_the_fortress_trigger_vesper_attacks_koji_action_000_002`
- English: `A brat piloting a giant renard is still just a brat.`
- Current Korean:
  `하![short_pause] 거대한 여우를 몰아 봐야 꼬맹이는 결국 [shaking]꼬맹이야.`

`Renard` may be a proper unit/species term, while the English sentence also
supports a literal fox reading. Other language resources do not establish a
shared Korean name, and the current wording is semantically understandable.
Keep deferred until the unit roster or codex confirms whether `Renard` is a
localized proper name.

## Decision

- Proposed editor changes: 0 keys.
- Deferred terminology findings: 1 item.
- No-edit findings: 9 sampled keys.
- No translation resource was modified.

The resource-level review of Campaign Air A1M3 is complete. The next scope
is Campaign Air A1M4.
