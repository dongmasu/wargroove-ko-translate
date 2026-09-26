# Translation Coverage Audit

Date: 2026-09-26

Scope: all generated Windows Wargroove 2 Korean string resources.
The audit compares the generated resource JSON against NSW English and
checks placeholders and markup tags. Identical values are findings for review,
not automatic translation errors; they include punctuation, numbers,
credits, language names, placeholders, and audio/developer identifiers.

## Summary

- Resources audited: 24
- Generated key entries: 15198
- Missing English keys: 0
- Empty Korean values: 22
- English/Korean identical values: 335
- Placeholder mismatches: 0
- Markup tag differences requiring review: 310

## Per Resource

| Resource | Keys | Missing | Empty | Identical | Placeholder mismatch | Markup differences |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `root` | 985 | 0 | 0 | 22 | 0 | 1 |
| `NPCs` | 113 | 0 | 0 | 1 | 0 | 0 |
| `birds` | 26 | 0 | 0 | 1 | 0 | 0 |
| `campaign_air` | 1752 | 0 | 0 | 55 | 0 | 51 |
| `campaign_earth` | 1975 | 0 | 0 | 64 | 0 | 41 |
| `campaign_final` | 627 | 0 | 0 | 7 | 0 | 40 |
| `campaign_sea` | 1641 | 0 | 0 | 38 | 0 | 53 |
| `campaign_tutorial` | 518 | 0 | 0 | 0 | 0 | 2 |
| `codex` | 237 | 0 | 0 | 0 | 0 | 0 |
| `codex_commanders` | 191 | 0 | 4 | 24 | 0 | 3 |
| `codex_lore_wg2` | 62 | 0 | 0 | 0 | 0 | 2 |
| `codex_units` | 479 | 0 | 0 | 0 | 0 | 0 |
| `conquest` | 972 | 0 | 0 | 12 | 0 | 42 |
| `dev` | 47 | 0 | 0 | 0 | 0 | 0 |
| `gallery` | 93 | 0 | 0 | 0 | 0 | 0 |
| `grooves` | 22 | 0 | 0 | 0 | 0 | 0 |
| `new_VO_lines` | 1022 | 0 | 7 | 0 | 0 | 0 |
| `secret` | 167 | 0 | 0 | 0 | 0 | 0 |
| `structures` | 30 | 0 | 0 | 0 | 0 | 1 |
| `ui` | 1021 | 0 | 0 | 66 | 0 | 0 |
| `ui_cutscene` | 2012 | 0 | 0 | 0 | 0 | 74 |
| `wargroove2` | 904 | 0 | 11 | 3 | 0 | 0 |
| `wargroove2_dev` | 206 | 0 | 0 | 38 | 0 | 0 |
| `zz_append` | 96 | 0 | 0 | 4 | 0 | 0 |

## Interpretation

- Missing keys and placeholder mismatches must be zero before release.
- Empty values remain deferred only when the source value is also
  intentionally blank or its runtime role is unknown.
- Markup tag differences are retained for semantic/UI review because
  Halley tags may be toggles or explicit open/close pairs.
- Identical values were separately classified in the review reports.
- This audit does not replace Windows runtime checks for clipping,
  font rendering, language selection, or fallback behavior.
