# Translation Batch 021: Campaign Air A2M1 Review

Date: 2026-09-27

## Scope

This is a read-only review of Campaign Air A2M1, `The Dead of Night`,
covering the opening presentation, Ragna/Vesper dialogue, Valder's speech,
and map metadata. The review compares English with Japanese and Simplified
Chinese references and checks Korean meaning, character voice, terminology,
and markup.

No translation resource was modified.

## Proposed Changes

### A2M1-001: untranslated French form of address

- Key:
  `wg2_a2m1_the_dead_of_night_trigger_talk_to_vesper_action_000_002`
- English: `All right, [wavy]ma protégée,[wavy] just like you've practiced!`
- Japanese: `愛弟子。練習したとおりにやるのよ。`
- Current Korean:
  `좋아, [wavy]ma protégée,[wavy] 연습한 대로만 해!`
- Proposed Korean:
  `좋아, [wavy]내 제자야,[wavy] 연습한 대로만 해!`
- Issue: untranslated player-facing address
- Reason: The French phrase means “my protégée” or “my apprentice.”
  Japanese and Chinese translate the relationship, while the current Korean
  leaves the phrase untranslated. The proposed wording preserves Vesper's
  affectionate yet instructive tone and the wavy markup.
- Status: `수정`
- Confidence: high

### A2M1-002: progress described unnaturally

- Key:
  `wg2_a2m1_the_dead_of_night_trigger_valder_speech_action_013_002`
- English: `Ragna is well on her way, mastering Fumomancy in just three years!`
- Current Korean:
  `라그나는 잘 나아가고 있습니다. 단 3년 만에 연기 조종을 통달했지요!`
- Proposed Korean:
  `라그나는 착실히 성장하고 있습니다. 단 3년 만에 연기 조종을 통달했지요!`
- Issue: naturalness
- Reason: `잘 나아가고 있습니다` is a literal and awkward rendering of
  being well on one's way. `착실히 성장하고 있습니다` expresses Ragna's
  progress naturally while preserving the following deliberately overstated
  claim of mastery.
- Status: `수정`
- Confidence: high

### A2M1-003: `force you to do their bidding`

- Key:
  `wg2_a2m1_the_dead_of_night_trigger_valder_speech_action_020_002`
- English: `No more shall cowardly Fell Lords force you to do their bidding...`
- Current Korean:
  `더는 비겁한 펠 군주들이 여러분에게 명령을 [shaking]강요하지[shaking] 못할 것입니다...`
- Proposed Korean:
  `더는 비겁한 펠 군주들이 여러분을 [shaking]억지로 부리지[shaking] 못할 것입니다...`
- Issue: naturalness and meaning
- Reason: `명령을 강요하다` is redundant and does not express being made
  to carry out someone else's will. `억지로 부리다` better conveys the
  political oppression described by `do their bidding`, while preserving the
  shaking emphasis.
- Status: `수정`
- Confidence: high

## Deferred Findings

### A2M1 title: `The Dead of Night`

- Key: `wg2_campaign_mapname_a2m1_the_dead_of_night`
- Current Korean: `깊은 밤`
- Japanese: `死者も眠る夜`

The Korean is a natural title but omits the explicit dead/undead imagery
present in Japanese and the campaign context. Keep deferred until campaign
title terminology is reviewed as a group; do not change this isolated label.

### `Fumomancy` terminology

The current Korean uses `연기 조종`, while Japanese and Chinese use forms
closer to smoke magic. The Korean is understandable and appears repeatedly
in A2M1. Keep deferred for a glossary-wide terminology decision.

## No Edit

The following sampled items were checked and require no wording change:

- `wg2_a2m1_the_dead_of_night_trigger_valder_speech_action_004_002`
  - `나는 죽어 가고 있습니다.` accurately sets up the delayed joke in the
    following `...언젠가는 말입니다.` line.
- `wg2_a2m1_the_dead_of_night_trigger_valder_speech_action_009_002`
  - `뼈를 떨지 마십시오!` appropriately preserves the undead wordplay in
    `Rattle not!`.
- `wg2_a2m1_the_dead_of_night_trigger_groove_targets_appear_action_006_002`
  - The exaggerated special-move title is localized creatively and retains
    the colour and wavy tags.
- `wg2_a2m1_the_dead_of_night_trigger_talk_to_valder_action_001_002`
  - The Korean correctly preserves Ragna's irritation at the whole Fortress
    being invited.
- `wg2_a2m1_the_dead_of_night_trigger_talk_to_vesper_action_008_002`
  - `곁에 있어 줘서 고마워. 날 포기하지 않아 줘서.` naturally preserves
    the emotional confession.
- `wg2_campaign_mapdescription_a2m1_the_dead_of_night`
  - The map description accurately conveys Vesper remembering how events
    began while travelling with Ragna.

Status for these items: `문제 없음`.

## Decision

- Proposed editor changes: 3 keys.
- Deferred terminology/title findings: 2 items.
- No-edit findings: 6 sampled keys.
- No translation resource was modified.
- The three proposed changes require approver approval before editing.

The next review scope is Campaign Air A2M2.
