# Translation Batch 018: Campaign Air A1M3 Opening Review

Date: 2026-09-27

## Scope

This is a read-only review of the Campaign Air A1M3 opening and the
Vesper confrontation. The review checks Korean meaning, character voice,
naturalness, and preservation of colour and emphasis markup against the
Windows WG2 English resource and Japanese/Simplified Chinese references.

No translation resource was modified.

## Proposed Changes

### A1M3-001: natural possessive in Vesper's greeting

- Key:
  `wg2_a1m3_the_fortress_cutscene_a1m3_scene_2_confronting_vesper_dialog_036_text`
- English: `How wonderful to see you again! Here! In your own home!`
- Current Korean:
  `다시 뵈어 [wavy]정말 반갑네요![wavy] 여기서! 경의 집에서!`
- Proposed Korean:
  `다시 뵈어 [wavy]정말 반갑네요![wavy] 여기서! 발더 경의 집에서!`
- Issue: naturalness
- Reason: `경의 집` is a one-off possessive use that is not otherwise
  established in A1M3. The approved exception uses the established title
  `발더 경` and preserves Vesper's pointed emphasis on Valder's own home.
- Status: `수정`
- Confidence: approved exception

### A1M3-002: `vessel` used as a physical companion

- Key:
  `wg2_a1m3_the_fortress_cutscene_a1m3_scene_2_confronting_vesper_dialog_064_text`
- English: `If you wish to accompany this vessel, we depart at once.`
- Current Korean:
  `[colour:purple]이 그릇과 동행하고 싶다면, 우리는 지금 떠난다.`
- Proposed Korean:
  `[colour:purple]이 육신과 함께하고 싶다면, 우리는 지금 떠난다.`
- Issue: naturalness and context
- Reason: In this scene, `vessel` refers to the body Vesper is inhabiting.
  `그릇과 동행하다` reads as physically travelling with a bowl or container.
  `육신과 함께하다` conveys the possessed body while preserving the
  detached, ominous voice.
- Status: `수정`
- Confidence: high

### A1M3-003: thanking someone for the vessel

- Key:
  `wg2_a1m3_the_fortress_cutscene_a1m3_scene_2_confronting_vesper_dialog_081_text`
- English: `I suppose I must thank you for this vessel.`
- Current Korean:
  `[colour:purple]이 그릇에 대해서는 [wavy]고맙다고[wavy] 해야겠군.`
- Proposed Korean:
  `[colour:purple]이 육신을 준 것에는 [wavy]고맙다고[wavy] 해야겠군.`
- Issue: meaning and naturalness
- Reason: `그릇에 대해서는 고맙다고 하다` is not a natural Korean
  construction and treats the vessel as an object of discussion rather than
  something Vesper received. The proposed wording makes the gratitude
  relationship explicit and preserves the emphasis tag.
- Status: `수정`
- Confidence: high

### A1M3-004: `service` mistranslated as volunteering

- Key:
  `wg2_a1m3_the_fortress_cutscene_a1m3_scene_2_confronting_vesper_dialog_086_text`
- English: `You have done me an incredible service... however unintended.`
- Current Korean:
  `[colour:purple]네가 내게 [wavy]엄청난[wavy] 봉사를 한 셈이다... 의도야 어떻든.`
- Proposed Korean:
  `[colour:purple]네가 내게 [wavy]엄청난[wavy] 도움을 준 셈이다... 의도야 어떻든.`
- Issue: word meaning
- Reason: In this context, `service` means a great favour or benefit, not
  `봉사` as volunteer work. `도움을 준 셈이다` matches the surrounding
  explanation that Ragna unintentionally provided Vesper's vessel.
- Status: `수정`
- Confidence: high

### A1M3-005: lost intensity in the airship boast

- Key:
  `wg2_a1m3_the_fortress_cutscene_a1m3_scene_2_confronting_vesper_dialog_138_text`
- English: `We can do it. My airship's more than fast enough!`
- Current Korean:
  `할 수 있어. 내 비행선은 [shaking]충분히[shaking] 빠르니까!`
- Proposed Korean:
  `할 수 있어. 내 비행선은 [shaking]훨씬[shaking] 빠르니까!`
- Issue: emphasis and meaning
- Reason: `more than fast enough` is stronger than merely `fast enough`.
  `훨씬 빠르니까` preserves the boastful excess and the shaking emphasis.
- Status: `수정`
- Confidence: high

## No Edit

The following sampled items were checked and require no wording change:

- `wg2_a1m3_the_fortress_cutscene_a1m3_scene_2_confronting_vesper_dialog_085_text`
  - `산 자들과 달리 순종하지` correctly contrasts the obedient vessel with
    the living.
- `wg2_a1m3_the_fortress_cutscene_a1m3_scene_2_confronting_vesper_dialog_109_text`
  - `정말로 '우리'가 맞다면 말이지만` preserves the uncertainty around
    Vesper becoming part of `we`.
- `wg2_a1m3_the_fortress_cutscene_a1m3_scene_2_confronting_vesper_dialog_133_text`
  - `열기구` is the established Korean term for `Balloon`.
- `wg2_a1m3_the_fortress_cutscene_a1m3_scene_2_confronting_vesper_dialog_136_text`
  - `불모기가 계속되게 둘 수는 없습니다` correctly conveys preventing the
    Fallow from continuing.
- `wg2_campaign_mapobjective_a1m3_the_fortress`
  - `발더에게 가라` is a concise and correct campaign objective.

Status for these items: `문제 없음`.

## Decision

- Proposed editor changes: 5 keys.
- No-edit findings: 5 sampled keys.
- No translation resource was modified.
- The five proposed changes require approver approval before editing.

The next review scope is the remaining A1M3 tutorial and combat-trigger text,
with special attention to Ballista warnings and repeated Vesper dialogue.
