# Translation Batch 009: Format-Token Findings

Date: 2026-09-27

## Scope

The 59 `{n}` order-change candidates from Batch 008 were compared sentence by
sentence against the English source. No translation resource was modified.

## Result

The reordered tokens are generally intentional Korean grammar changes:

- subjects and locations move before the predicate;
- owners and players move before the owned unit or action;
- operators and values move into natural Korean order;
- action descriptions place the target object before the verb;
- trigger-readable labels preserve every `{n}` token exactly once.

No token was found to be dropped, duplicated, or substituted with another
index.

## Confirmed Semantic Finding

Status: `수정` candidate, awaiting approval

Key:

```text
trigger_action_readable_set_weather
```

English:

```text
Set the current weather to {0} in {1} days.
```

Current Korean:

```text
{1}일 동안 현재 날씨를 {0}(으)로 설정합니다.
```

The current wording means “set the weather for `{1}` days,” while the English
means “set the weather after `{1}` days.” Proposed Korean:

```text
{1}일 후 현재 날씨를 {0}(으)로 설정합니다.
```

This is a semantic translation issue, not a token-order issue.

## Reviewed Without Token Error

The remaining 58 format-token reorderings preserve the source parameter
identity and are accepted as intentional display-order changes for this
review stage. They still remain subject to overall Korean naturalness review,
especially the trigger-readable labels:

- `trigger_action_readable_transfer_gizmo_state`
- `trigger_action_readable_set_unit_spent`
- `trigger_action_readable_transfer_gold`
- `trigger_action_readable_transfer_health`
- `trigger_condition_readable_check_gizmo_state`

These labels may need wording improvements, but the current evidence does not
justify changing them as a format-token defect.

## Approval Boundary

Only `trigger_action_readable_set_weather` is proposed for an editor change.
The editor must wait for approval of that exact key and proposed Korean text.
After editing, the verifier must confirm the `{0}` and `{1}` tokens and rerun
the resource tests.
