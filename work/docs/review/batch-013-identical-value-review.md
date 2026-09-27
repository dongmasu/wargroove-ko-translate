# Translation Batch 013: English/Korean Identical Value Review

Date: 2026-09-27

## Scope

This is a read-only review of values where the current Korean resource is
identical to the Windows WG2 English source. The historical coverage report
listed 335 candidates. Re-running the comparison against the current work tree
produces 323 candidates; the current reproducible count is used below.

No translation resource was modified.

## Classification

| Class | Count | Decision |
| --- | ---: | --- |
| Control tags, punctuation, pauses, and effect-only dialogue | 211 | Intentional source reuse; no edit |
| Technical and metadata values | 112 | Intentional source reuse; no edit |
| Total | 323 | No translation candidate |

No candidate is an ordinary English sentence or paragraph that is visibly
untranslated in the Korean resource.

## Control and Effect Values

The 211 values contain only markup, punctuation, spacing, or short
non-lexical delivery content after control tags are removed. Examples include:

- `[slow]. . .`
- `.[short_pause].[short_pause].`
- `[instant][shaking]   !`
- `[wavy][colour:player_purple]   . [short_pause]. [short_pause].`

These values encode silence, hesitation, reaction timing, or punctuation-only
dialogue. Translating them would either be meaningless or risk changing the
delivery behavior. Status: `문제 없음`.

## Technical and Metadata Values

The remaining 112 values are non-prose values with stable runtime or display
semantics:

- 46 audio-event and developer identifiers such as `caesar_growl`,
  `mercival_ghost_laugh3`, and `nuruShoutSurprise`;
- 7 encoded or binary technical strings;
- 20 credits and company names;
- 14 language names displayed in their native form;
- 13 commander height values such as `109 cm`;
- 10 UI notation values such as `CPU 1`, `P1`, `2v2`, `OK`, and `x{0}`;
- 2 runtime placeholders such as `#character_prisoner_name` and related
  campaign marker values.

These values are identifiers, proper names, measurements, language labels,
game notation, or runtime substitutions rather than translatable prose.
Status: `문제 없음`.

## Specific Checks

### Game notation

`300 G` and `100 G` are currency-choice values. `G` is part of the source
notation and should not be translated without evidence that Windows expects a
localized currency suffix.

### Runtime placeholders

`#character_prisoner_name` is a runtime substitution marker and must remain
byte-for-byte unchanged. The same rule applies to `{0}`, `{1}`, and other
format values in identical UI strings.

### Audio identifiers

Values such as `caesar_growl`, `ragna_what`, and
`mercival_ghost_verywellthen` are lookup identifiers. Changing them would
break audio or event linkage even though they are visible in the string
resources.

### Language labels and credits

Native language names and company/credit names are intentionally displayed
without Korean translation. Their equality with English is not a translation
defect.

## Decision

- Current identical-value scope: 323.
- Actual ordinary English prose left untranslated: 0.
- Approved edits: none.
- All 323 candidates are classified as `문제 없음`.
- The historical count of 335 remains a prior audit count and must not be
  used as the current edit scope.

The next review target is the remaining campaign and UI naturalness pass,
starting with strings that are translated but may have continuity, terminology,
or context problems rather than token-level differences.
