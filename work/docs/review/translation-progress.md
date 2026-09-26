# Wargroove 2 Korean Translation Progress

Date: 2026-09-26
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

## Deferred / Release Gate

- Custom TTF/OTF to Halley font conversion.
- `ui.dat` replacement unless runtime font issues appear.
- Blank, developer-only, audio-cue, and corrupted-looking internal keys until
  their runtime role is confirmed.
- Final Windows smoke test of the exact generated pack.

## Current Artifacts

- Direct Windows release pack:
  `dist/Wargroove 2/1.2.x/20260926/config.dat`
- Release pack SHA-256:
  `746b17b14cb52dcbd3d9e94ca33d8400e2bae6555d564b66a40a6661a456bbc6`
- Release pack manifest:
  `work/docs/review/Wargroove2-1.2.x-20260926-config-manifest.json`
- Release pack index:
  `work/docs/review/Wargroove2-1.2.x-20260926-config-index.json`
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
  `work/docs/review/release-report-2026-09-26.md`
