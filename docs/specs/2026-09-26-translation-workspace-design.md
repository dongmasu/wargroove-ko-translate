# Wargroove Korean Translation Workspace Design

**Date:** 2026-09-26

## Goal

Create a lightweight workspace for translating the Windows version of
Wargroove 2 into Korean. macOS is out of scope. Wargroove 1 is officially
localized in Korean and can be used as a terminology and style reference.

## Constraints

- Do not use a `po/` directory.
- Do not assume the Wargroove 2 source format or translation method before
  inspecting the Windows game files.
- Preserve source files and existing translations by default.
- Do not perform automatic full rewrites or start the next work cycle
  automatically.
- The first setup must be a safe skeleton and must not require real game files.
- Keep credentials, local machine secrets, and external service integration out
  of the initial setup.

## Architecture

Start with a lightweight document-and-reference workspace. Add parsers,
configuration, scripts, or tests only after the target game's file format and
translation workflow are known.

## Current Layout

```text
README.md
PROJECT-AI.md
src/                  # immutable unpacked game sources
tools/                # HALLEYPK and ConfigFile tools
work/                 # editable translation work and work docs
dist/                 # dated distributable config.dat files
docs/                 # stable project documentation
references/           # local source material, Git-ignored
```

## Safety

- Do not modify source files or reference material by default.
- Any future write operation must require an explicit command and create a
  reversible backup or output copy.

## Analysis Workflow

The project has three deliberate analysis stages:

1. Extract the English, Japanese, Chinese, and Korean sections from the
   Windows Wargroove 1 files:
   `references/Wargroove/assets/config.dat` and `ui.dat`.
2. Extract the same language sections from the NSW Wargroove 2 patch files:
   `references/posts/WG2_KR/romfs/config.dat` and `ui.dat`.
3. Analyze the Windows Wargroove 2 files:
   `references/Wargroove 2/assets/config.dat` and `ui.dat`, and determine the
   structural changes needed to add Korean.

The NSW files must not be copied directly into the Windows Wargroove 2 files.
Wargroove 1's official Korean localization is the primary terminology
reference. The NSW patch is a secondary translation and structural reference.
English, Japanese, and Chinese are reference languages for translation, with
Japanese receiving particular attention because its word order is close to
Korean.

## Separation Rules

- `src/Wargroove <game>/<version>/config/` contains immutable readable source
  conversions; raw unpacked payloads belong under `work/docs/analysis/`
  and is never edited.
- `work/Wargroove <game>/<version>/config/` contains translation edits,
  generated payloads, and experiments for that target.
- `work/docs/` contains changing analysis, review, and release records.
- `dist/Wargroove <game>/<version>/<yyyymmdd>/` contains only files intended
  to be copied into the game.
