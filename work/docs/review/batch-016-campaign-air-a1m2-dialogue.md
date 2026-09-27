# Translation Batch 016: Campaign Air A1M2 Dialogue Review

Date: 2026-09-27

## Scope

This is a read-only review of the remaining player-facing dialogue in
Campaign Air mission A1M2, `Felheim in Fallow`. The review compares the
Windows WG2 English resource with the Japanese and Simplified Chinese
references and checks the current Korean for meaning, naturalness, and
recurring terminology.

No translation resource was modified.

## Proposed Changes

### A1M2-001: imagined-location question

- Key:
  `wg2_a1m2_felheim_in_fallow_cutscene_a1m2_scene_3_cozy_library_dialog_039_text`
- English: `Are you there?`
- Japanese: `想像できた？`
- Current Korean: `거기 도착했어?`
- Proposed Korean: `그곳에 있어?`
- Issue: context and naturalness
- Reason: The preceding lines ask Errol to imagine being in a safe, warm
  place. `도착했어?` describes physically arriving at a destination and
  changes the guided-imagery context. `그곳에 있어?` preserves the intended
  mental-location question without adding an explanation or changing the
  dialogue rhythm.
- Status: `수정`
- Confidence: high

### A1M2-002: idiom rendered as a nest

- Key:
  `wg2_a1m2_felheim_in_fallow_trigger_all_kids_near_oddvar_action_000_002`
- English: `[wavy]Ooh-hoo-hoo!![wavy][short_pause] At last, the children come home to roost.`
- Japanese: `幼子たちよ、過ちは自分の身に跳ね返るものだぞ。`
- Current Korean:
  `[wavy]우후후후![wavy][short_pause] 드디어 아이들이 제 둥지로 돌아왔구나.`
- Proposed Korean:
  `[wavy]우후후후![wavy][short_pause] 드디어 아이들이 제 발로 찾아왔구나.`
- Issue: idiom and naturalness
- Reason: `come home to roost` is an idiom, and `제 둥지` is an unnatural
  literal image for human children in this scene. The proposed wording
  retains Oddvar's predatory satisfaction that the children came within
  reach, while matching the following threat.
- Status: `수정`
- Confidence: high

### A1M2-003: `entered Fallow` sentence connection

- Key:
  `wg2_a1m2_felheim_in_fallow_cutscene_a1m2_scene_2_kids_land_dialog_029_text`
- English: `What's happening? Felheim's in [colour:player_3]Fallow,[colour:player_black] after 20 years of peace...`
- Japanese: `２０年間平和が続いた後、フェルハイムは[colour:player_3]喪失時代[colour:player_black]に入った…`
- Current Korean:
  `무슨 일이냐고요? 20년 평화 끝에 펠하임이 [colour:player_3]불모기에[colour:player_black] 들었습니다...`
- Proposed Korean:
  `무슨 일이냐고요? 20년간 평화가 이어진 뒤, 펠하임은 [colour:player_3]불모기에[colour:player_black] 접어들었습니다...`
- Issue: naturalness and source structure
- Reason: `20년 평화 끝에` is compressed and sounds like the peace itself
  ended abruptly. `20년간 평화가 이어진 뒤` clearly expresses the source's
  time relationship, and `불모기에 접어들다` is a more natural collocation
  than `불모기에 들다`.
- Status: `수정`
- Confidence: high

## Deferred Findings

### Fallow terminology

The recurring proper/lore term `Fallow` is currently `불모기`. Japanese uses
`喪失時代` and Simplified Chinese uses `沉寂期`, both of which emphasize a
named historical era rather than literal barrenness. The Korean term is
understandable and internally consistent, but changing it requires a
campaign-wide terminology decision. Keep deferred until the glossary and
all A1M2 occurrences are reviewed together.

### Bonus objective: `seasoned hunters`

- Key: `wg2_campaign_a1m2_felheim_in_fallow_bonus_objective_0`
- English: `Defeat Oddvar using a pair of seasoned hunters.`
- Current Korean: `노련한 사냥꾼 한 쌍으로 오드바르를 물리치기`
- Japanese: `狩猟犬２匹を使ってオドヴァルを倒す。`
- Simplified Chinese: `使用一对经验丰富的猎手消灭奥德瓦。`

The Japanese explicitly says two hunting dogs, while English and Chinese
describe experienced hunters. The resource text alone cannot establish
whether this is a mistranslated unit name or an intentional reference to
the Fenris and Donut dog units. Keep deferred until the A1M2 stage roster or
objective trigger is checked.

### `last Fell Lord`

- Key:
  `wg2_a1m2_felheim_in_fallow_cutscene_a1m2_scene_3_cozy_library_dialog_083_text`
- Current Korean: `--헤븐송이 [shaking]마지막[shaking] [colour:player_blue]펠 군주를 죽였을 때죠.`

Japanese and Simplified Chinese use `previous/former` rather than literally
`last`. This may be a lore distinction or a localization choice. Keep
deferred until the campaign's historical terminology is checked globally.

## No Edit

The following sampled items were checked and do not require a wording change:

- `wg2_a1m2_felheim_in_fallow_cutscene_a1m2_scene_3_cozy_library_dialog_013_text`
  - `왜 그러냐고?` is an acceptable emphatic repetition of `What's wrong?`.
- `wg2_a1m2_felheim_in_fallow_trigger_koji__40_health_action_003_002`
  - `황홀할 텐데` intentionally preserves Oddvar's disturbing interpretation
    of being close to death.
- `wg2_a1m2_felheim_in_fallow_trigger_villager_4_item_action_002_002`
  - `낡은 갑옷` follows the English reward setup; the different Japanese
    wording does not by itself prove a Korean error.
- `wg2_a1m2_felheim_in_fallow_trigger_villager_4_item_action_004_002`
  - The Korean item name correctly renders the girdle/belt and preserves the
    alliterative joke better than a literal armor rendering.

Status for these items: `문제 없음`.

## Decision

- Proposed editor changes: 3 keys.
- Deferred terminology/context findings: 3 items.
- No-edit findings: 4 sampled keys.
- No translation resource was modified.
- The three proposed changes require approver approval before editing.

The next review scope is the remaining A1M2 objective/runtime strings,
followed by Campaign Air A1M3 tutorial and dialogue text.
