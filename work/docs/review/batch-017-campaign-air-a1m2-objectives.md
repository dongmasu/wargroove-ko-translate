# Translation Batch 017: Campaign Air A1M2 Objectives and Runtime Text

Date: 2026-09-27

## Scope

This is a read-only review of the remaining Campaign Air A1M2 objective,
map-label, map-description, and runtime-trigger strings after the dialogue
review in Batch 016. The review checks source meaning, objective style,
markup, and consistency with the established Korean terminology.

No translation resource was modified.

## No Edit

The following strings were checked and require no wording change:

- `wg2_campaign_mapdescription_a1m2_felheim_in_fallow`
  - `펠하임 요새로 가는 길에, 구조대가 도움이 필요한 마을에 들른다.`
  - Correctly conveys that the Rescue Squad stops to help a village in need.
- `wg2_campaign_a1m2_felheim_in_fallow_bonus_objective_1`
  - `제재소를 모두 점거하기`
  - Correct objective-style rendering of capturing all Lumber Mills.
- `wg2_a1m2_felheim_in_fallow_trigger_objective_defeat_oddvar_action_000_000`
  - `[colour:player_blue]오드바르를 물리쳐라!`
  - Correct imperative objective and preserves the colour tag.
- `wg2_a1m2_felheim_in_fallow_trigger_oddvar_only_enemy_left_action_000_002`
  - `이제 하나 남았어!`
  - Natural and equivalent to the remaining-one trigger.
- `wg2_a1m2_felheim_in_fallow_trigger_oddvar_only_enemy_left_action_002_002`
  - `아니, 아니, 아니지... 때가 되면 내 아이들이 다시 일어날 테니...`
  - Preserves Oddvar's delayed-threat meaning and character voice.
- `wg2_a1m2_felheim_in_fallow_trigger_player_turn_4_koji_checks_in_action_007_002`
  - `[shaking]두 사람[shaking]이 동시에 추울 수도 있잖아, 올라![short_pause] 그건 되는 거야!`
  - Correctly preserves the joke and emphasis markup.
- `wg2_a1m2_felheim_in_fallow_trigger_lose_twins_die_action_006_002`
  - `그 [wavy]아름다운[wavy] 시신에서... 내가 새로이 낳아 주마!`
  - Faithful to the disturbing resurrection threat and preserves the tag.
- `wg2_a1m2_felheim_in_fallow_trigger_win_defeat_oddvar_action_003_002`
  - `그리고 너희 [shaking]누구도[shaking] 내 앞을 막지 못할 것이다!!`
  - Correctly carries the source's emphatic `NONE`.

Status for these items: `문제 없음`.

## Deferred Findings

### A1M2 map name and `Fallow`

- Key: `wg2_campaign_mapname_a1m2_felheim_in_fallow`
- English: `Felheim in Fallow`
- Current Korean: `불모기의 펠하임`

The map name is grammatically usable and matches the recurring Korean term,
but the term itself remains under review because Japanese `喪失時代` and
Simplified Chinese `沉寂` frame `Fallow` as a named historical era. Do not
change this isolated map label before making a campaign-wide terminology
decision. Status: `계속 보류`.

### A1M2 bonus objective

- Key: `wg2_campaign_a1m2_felheim_in_fallow_bonus_objective_0`
- Current Korean: `노련한 사냥꾼 한 쌍으로 오드바르를 물리치기`

The English and Chinese support the current Korean, while Japanese says
`two hunting dogs`. The stage roster or objective trigger must establish
whether this refers to Fenris and Donut before changing the objective.
Status: `계속 보류`.

## Decision

- Proposed editor changes: 0 keys.
- Deferred context/terminology findings: 2 items.
- No-edit findings: 8 sampled keys.
- No translation resource was modified.

The A1M2 text review is complete at the resource level. The next review
scope is Campaign Air A1M3 tutorial and dialogue text.
