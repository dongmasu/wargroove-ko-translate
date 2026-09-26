# Wargroove 2 Korean Translation Release Verification

Date: 2026-09-26

## Target

- Game: Windows Wargroove 2
- Version: `v1.2.12`
- Build: `#45031`
- Base: `references/Wargroove 2/assets/config.dat`
- Translation sources: Wargroove 1 official Korean resources and NSW
  Wargroove 2 Korean, English, Japanese, and Simplified Chinese resources

## Generated Package

- Output: `dist/Wargroove 2/1.2.x/20260926/config.dat`
- Manifest: `work/docs/review/Wargroove2-1.2.x-20260926-config-manifest.json`
- Index: `work/docs/review/Wargroove2-1.2.x-20260926-config-index.json`
- Base assets: `3,514`
- Final assets: `3,538`
- Added Korean resources: `24`
- AES payload: present; original Windows IV preserved
- SHA-256:
  `746b17b14cb52dcbd3d9e94ca33d8400e2bae6555d564b66a40a6661a456bbc6`

## Translation Verification

- Korean resource keys: `15,198`
- Format placeholder check: passed
- Resource key check: passed
- All 24 generated Korean payloads decoded successfully
- Decoded Korean key count: `15,198`
- Full resource audit:
  `work/docs/review/translation-coverage-2026-09-26.md`
- Audit result: 24 resources, 15,198 entries, 0 missing English keys, and
  0 placeholder mismatches
- Campaign-air pass: completed
- Three confirmed untranslated French/source strings were translated:
  `Mon dieu...` -> `아이고...`
  `C'est impossible!` -> `말도 안 돼!`
  Batch 005 also translated one complete French/source conquest line.
- Remaining identical English/Korean values were classified as intentional
  punctuation, audio cues, placeholders, developer identifiers, numeric data,
  credits, or language names.
- Structural missing-key additions are documented separately; four damaged
  campaign keys remain semantic placeholders (`???`) pending source/runtime
  confirmation.
- Batch 005 review:
  `work/docs/review/batch-005-untranslated-source.md`

## Technical Verification

Passed:

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Result: 13 tests passed.

The generated pack was reopened with `halleypk.py`. All 24 added payloads
matched their source files, the output contained 3,538 indexed assets, and
the encrypted campaign-air and conquest payloads decoded with the updated
Korean strings.

## Windows Final Smoke Test

This is the remaining release gate and must be performed on Windows using a
copy of the installed game:

1. Back up the original `config.dat`.
2. Replace only the test copy's `assets/config.dat` with
   `dist/Wargroove 2/1.2.x/20260926/config.dat`.
3. Launch Wargroove 2 and select Korean in language settings.
4. Check the title/menu, campaign objectives, campaign dialogue, codex,
   unit/commander information, settings, and map UI.
5. Check clipping, missing glyphs, fallback-to-English strings, crashes, and
   save/load behavior.
6. Restore the original file after testing, unless the test result is
   explicitly approved for release.

The earlier experimental AES pack rendered Korean text successfully in
Windows. That result does not replace testing the final hash above.

### Result Record

The following rows must be updated from `PENDING` only after testing the exact
release hash above on Windows build `#45031`:

| Test ID | Area | Expected evidence | Status |
| --- | --- | --- | --- |
| W01 | Launch/menu | Game starts; Korean menu appears | PENDING |
| W02 | Language selection | Korean remains selected after restart | PENDING |
| W03 | Campaign | Objectives and dialogue display Korean | PENDING |
| W04 | Codex/unit info | Codex and unit descriptions display Korean | PENDING |
| W05 | UI layout | No clipping, overflow, or missing glyph boxes | PENDING |
| W06 | Font rendering | Korean glyphs render with the selected font | PENDING |
| W07 | Stability | No crash during launch, map load, save/load | PENDING |
