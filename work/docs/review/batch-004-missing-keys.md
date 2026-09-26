# Translation Batch 004: Missing Resource Keys

Date: 2026-09-26

## Applied

The following unambiguous keys were absent from the NSW Korean resources and
were added to the generated Korean resources:

- UGC player-count filters: `1`, `2`, `3`, `4`
- Codex commander ages: 7, 60, 121, 13, 24, 30, 49, 13, 37, 39, 39
- UI booleans: `false`, `true`
- Short turn label: `턴 `
- Four structurally corrupted campaign-air keys: `???` placeholders with
  original markup preserved
- Blank campaign objectives/descriptions, blank codex fields, blank Nadia
  voice labels, blank character titles/tooltips, and developer voice cue
  identifiers were added with their source-compatible blank or identifier
  values

Generated Korean string coverage increased from 15,110 to 15,198 keys.

## Semantic Deferrals

The following keys are now structurally present but are not claimed as
translated:

- four campaign air entries with corrupted-looking internal names/source text;
- blank campaign objectives and descriptions;
- blank character birthday fields;
- blank Nadia voice cue labels;
- blank character title/tooltips;
- developer-only voice cue identifiers.

The four corrupted campaign-air entries use `???` because English, Japanese,
and Chinese contain the same damaged source symbols. The blank and voice-cue
entries preserve their source semantics. Runtime confirmation is still
required before release.
