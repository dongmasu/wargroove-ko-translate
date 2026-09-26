# Wargroove Korean Translation

This repository is a project for creating a Korean translation for the Windows
version of Wargroove 2. macOS is not a supported platform for this project.

Wargroove 1 has an official Korean translation, while Wargroove 2 does not
support Korean. Wargroove 1 may be used as a terminology and style reference.

## Links

- Official website: https://wargroove.com/
- Wargroove 1 on Steam: https://store.steampowered.com/app/607050/_/
- Wargroove 2 on Steam: https://store.steampowered.com/app/1346020/Wargroove_2/

## Principles

- Preserve source files and existing translations by default.
- Keep source and translation work organized by the actual target game's needs.
- Keep credentials, machine secrets, and external services out of the
  workspace.

## Layout

```text
src/
  Wargroove 1/2.1.x/    Immutable Wargroove 1 source snapshot
  Wargroove 2/1.2.x/    Immutable Windows WG2 source snapshot
tools/                  HALLEYPK parser and ConfigFile tools
tests/                  Regression tests and small test fixtures
work/
  Wargroove 1/2.1.x/    Wargroove 1 working copy
  Wargroove 2/1.2.x/    WG2 translation working files
  docs/                  Analysis, readable payloads, review, and release records
dist/                   Dated files ready to copy into the game
docs/                   Stable project design and process documents
references/             Local source material, excluded from Git
```

Files under `src/` are immutable, readable source snapshots. Raw unpacked
payloads and intermediate conversions belong under `work/docs/analysis/`.
Translation edits belong under the matching `work/<game>/<version>/config/`
directory.
Only the dated `config.dat` under `dist/` is a release artifact.

The complete DAT-and-ZIP packaging rule is documented in
[`docs/dist-packaging.md`](docs/dist-packaging.md). Build a Wargroove 2
release with:

```sh
python3 tools/build_dist_package.py
```

The translation workflow is defined in
[`docs/translation-process.md`](docs/translation-process.md).
It uses the reviewer, approver, editor, verifier, and publisher separation
established in the related Wesnoth translation project.
