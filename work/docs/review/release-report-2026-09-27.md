# Wargroove 2 Korean Translation Release Verification

Date: 2026-09-27

## Target

- Game: Windows Wargroove 2
- Version: `v1.2.12`
- Build: `#45031`
- Base workspaces: `work/Wargroove 2/1.2.x/config` and `ui`

## Generated Package

- Output directory: `dist/Wargroove 2/1.2.x/20260927/`
- ZIP: `Wargroove2-ko-translate-1.2.x-20260927.zip`
- `config.dat`: 3,538 assets, 24 Korean resources
- `ui.dat`: 2,662 assets
- ZIP contents: `assets/config.dat`, `assets/ui.dat`, `INSTALL.md`
- `config.dat` SHA-256:
  `8c02540734268741a41f3c0a73c93ff948e3ac231f6672d6cb789ace1ce66be2`
- `ui.dat` SHA-256:
  `51f937f207f61d4ff55eb223134f338d9748b04844ebe0e3e94421ad41b47a38`
- ZIP SHA-256:
  `aa74be233de4e9e4e58396319a19ee7b3de5cfdb25b7bc93148132a1ead360fa`

## Translation Verification

- Korean resource count: 15,198 keys
- Campaign-air review: A1M1 through A3M2 complete
- Approved editor changes: 23
- Format placeholders, markup, and control-code checks: passed
- `발더 경의 집에서!` exception recorded in `translation-exceptions.tsv`
- Deferred findings remain documented and were not silently changed.

## Font Verification

- Only `Noto Serif` and `fontTex/Noto Serif` were changed in `ui.dat`.
- `Sitka Text Bold Italic` and all other UI font assets remain unchanged.
- Source: Google Noto Serif Korean Regular
- Rasterization: 42 px
- Atlas: 4096 x 2387
- Output: single-channel SDF
- The original Noto Serif contains only 51 Hangul syllables, so `config.dat`
  and `ui.dat` must be installed together.

## Automated Checks

Passed:

```text
python3 -m unittest discover -s tests -p 'test_*.py'
31 tests OK
git diff --check
```

The generated package was reopened successfully. The encrypted `config.dat`
contains 3,538 indexed assets, and the `ui.dat` contains both Noto Serif
assets and 2,662 total entries.

## Windows Smoke Test

Pending. This macOS environment cannot launch the Windows game. The exact
package should be tested on Windows for launch, language selection, campaign
dialogue, UI clipping, glyph rendering, and save/load stability before any
claim of runtime verification.
