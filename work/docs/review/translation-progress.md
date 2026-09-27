# Wargroove 2 Korean Translation Progress

Date: 2026-09-27
Target: Windows Wargroove 2 `v1.2.12`, build `#45031`

## Review Complete

- Parsed and decoded all 24 NSW Korean string resources.
- Built a 15,198-key Korean Windows resource set.
- Applied Wargroove 1 continuity terminology and recorded 15 context decisions.
- Applied UI and campaign-air naturalness corrections.
- Translated one additional complete French/source line in the conquest
  resource and recorded the 22 evidence-backed empty-value deferrals.
- Added 18 unambiguous translation/data keys and 70 structural missing keys.
- Preserved format placeholders and validated markup/control-code-sensitive
  edits.
- Added ModPacker-compatible AES/CBC handling to `halleypk.py`.
- Verified Windows WG2 encrypted `config.dat` round-trip with 3,514 assets.
- Generated a Windows release pack with 24 Korean resources and 3,538 total
  assets.
- Confirmed Korean text rendering in Windows WG2.
- Documented `ui.dat`, font selection, and Halley font format.

## Packaging Complete

- Campaign-air dialogue naturalness and continuity review.
- Cross-resource terminology consistency pass for names, titles, factions,
  units, structures, grooves, and recurring UI terms.
- Regeneration of all 24 Korean resources and the Windows direct-replacement
  pack.

The campaign-air pass also resolved two untranslated French exclamations:
`Mon dieu...` -> `아이고...` and `C'est impossible!` -> `말도 안 돼!`.
Batch 005 also translated one complete French/source conquest line.
Remaining identical English/Korean values were classified as punctuation,
audio cues, developer identifiers, placeholders, numbers, credits, or
language names rather than translation omissions.

## Campaign Air QA Complete

- Completed resource-level review for A1M1 through A3M2.
- Added review reports Batch 014 through Batch 026.
- Applied all 23 approved editor changes to the Korean campaign-air resource
  and synchronized the verified resource.
- Recorded the A1M3 `발더 경의 집에서!` wording as a versioned exception.
- Recorded deferred terminology, runtime-context, and corrupted-placeholder
  findings separately from confirmed wording issues.
- Confirmed no format-tag mismatch in the newly reviewed A2M1-A3M2 batches.
- `tests/test_translation_resources.py`: 4 tests passed.
- `git diff --check`: passed.

Verifier review and package smoke testing of the edited resources are
complete.

## Deferred / Release Gate

- Windows smoke test of the exact generated package remains pending because
  this environment cannot launch the Windows game.
- Blank, developer-only, audio-cue, and corrupted-looking internal keys until
  their runtime role is confirmed.

## Current Artifacts

- Direct Windows release pack:
  `dist/Wargroove 2/1.2.x/20260927/assets/config.dat`
- `config.dat` SHA-256:
  `c653c487a29c564a7c9f0f2d14a99b372f6d21879b8e2532008b0224c28d718f`
- `ui.dat` SHA-256:
  `06224bc3d513136f3111c1f59823f1294793867dcbb1e8cf87a1601290939331`
- ZIP SHA-256:
  `b315cba96b4de1666b66ebcf89388aff346e4642206f85730d3ec6c238038da9`
- Terminology review:
  `work/docs/review/batch-001-terminology.md`
- UI review:
  `work/docs/review/batch-002-ui-residue.md`
- Campaign review:
  `work/docs/review/batch-003-campaign-air-naturalness.md`
- Missing-key review:
  `work/docs/review/batch-004-missing-keys.md`
- Untranslated-source review:
  `work/docs/review/batch-005-untranslated-source.md`
- Release verification:
  `work/docs/review/release-report-2026-09-27.md`
