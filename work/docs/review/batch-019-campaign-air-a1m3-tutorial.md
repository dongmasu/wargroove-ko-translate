# Translation Batch 019: Campaign Air A1M3 Tutorial and Combat Review

Date: 2026-09-27

## Scope

This is a read-only review of the remaining Campaign Air A1M3 unit tutorials,
combat-trigger dialogue, and Ballista warnings. The review checks Korean
naturalness, quantity placeholders, gameplay meaning, and preservation of
markup against the Windows WG2 English resource and Japanese/Simplified
Chinese references.

No translation resource was modified.

## Proposed Changes

### A1M3-001: transport capacity quantity expression

- Key:
  `wg2_a1m3_the_fortress_trigger_balloon_tutorial_action_001_002`
- English: `This transport unit carries up to -2- units that normally travel on foot.`
- Current Korean:
  `이 수송 유닛은 보통 도보로 이동하는 유닛을 최대 -2- 기까지 태울 수 있습니다.`
- Proposed Korean:
  `이 수송 유닛은 보통 도보로 이동하는 유닛을 최대 -2-기까지 태울 수 있습니다.`
- Issue: spacing and quantity expression
- Reason: The space between the numeric placeholder and the Korean unit
  counter breaks the quantity expression. The proposed form preserves the
  `-2-` placeholder exactly and renders the intended `up to 2 units`.
- Status: `수정`
- Confidence: high

### A1M3-002: Mage healing target quantity

- Key:
  `wg2_a1m3_the_fortress_trigger_mage_tutorial_action_002_002`
- English: `Their Special Ability Heals up to -5- adjacent allies. (Cost: 300 G)`
- Current Korean:
  `[colour:player_black]특수 능력으로 인접한 아군을 최대 -5- 기까지 [wavy]치유[wavy]합니다. (비용: 300 G)`
- Proposed Korean:
  `[colour:player_black]특수 능력으로 인접한 아군 유닛을 최대 -5-기까지 [wavy]치유[wavy]합니다. (비용: 300 G)`
- Issue: quantity expression and gameplay clarity
- Reason: `인접한 아군을 ... 기까지` mixes a person-like noun with a unit
  counter and leaves the target type implicit. `아군 유닛을 최대 -5-기까지`
  clearly describes the affected units while preserving the cost and wavy
  markup.
- Status: `수정`
- Confidence: high

## No Edit

The following sampled strings were checked and require no wording change:

- `wg2_a1m3_the_fortress_trigger_balloon_tutorial_action_000_002`
  - `열기구 유닛을 살펴볼까요?` correctly uses the established Balloon term.
- `wg2_a1m3_the_fortress_trigger_mage_tutorial_action_001_002`
  - `마법사는 공중 유닛에게 [shaking]치명적인[shaking] 피해를 줍니다.`
    correctly conveys the severe Air-unit damage and preserves emphasis.
- `wg2_a1m3_the_fortress_trigger_defeat_a_ballista_action_000_002`
  - `발리스타 하나, 격파!` is concise combat callout text.
- `wg2_a1m3_the_fortress_trigger_warn_player_not_to_send_aeronauts_unaided_action_001_002`
  - The range warning and wing-destruction consequence are accurately
    conveyed, including both colour tags.
- `wg2_a1m3_the_fortress_trigger_warn_player_not_to_send_balloon_unaided_action_002_002`
  - The warning that carried units are lost with a destroyed transport is
    clear and gameplay-accurate.
- `wg2_a1m3_the_fortress_trigger_twins_seriously_hurt_action_000_002`
  - `멍청하고 얼빠진 것들, 정말 [shaking]지긋지긋해...` preserves Vesper's
    irritated insult and emphasis.
- `wg2_a1m3_the_fortress_trigger_vesper_seriously_injured_action_002_002`
  - `우리 [wavy]대화로[wavy] 풀면 안 될까?` is a natural negotiation line
    and preserves the wavy tag.
- `wg2_a1m3_the_fortress_trigger_zone_1_ballista_kills_player_aeronaut_action_000_002`
  - `손해가 크다` correctly communicates that losing the unit has a cost.

Status for these items: `문제 없음`.

## Internal/Developer Text

The A1M3 tutorial contains two visible developer notes:

- `DEVNOTE: LINK TO CODEX BROKEN`
- `DEVNOTE: CODEX LINK BROKEN`

They are already translated as `DEVNOTE: 코덱스 링크가 끊김`. These remain
internal/developer strings rather than player-facing prose and require no
additional wording change.

## Decision

- Proposed editor changes: 2 keys.
- No-edit findings: 8 sampled keys.
- Internal/developer findings: 2 keys, no change.
- No translation resource was modified.
- The two proposed changes require approver approval before editing.

The next review scope is the remaining A1M3 objective and repeated combat
triggers, followed by Campaign Air A1M4.
