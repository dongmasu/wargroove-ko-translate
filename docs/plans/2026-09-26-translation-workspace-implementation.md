# Translation Workspace Implementation Plan

> **For agentic workers:** This plan was executed inline in the current session.

**Goal:** Analyze Wargroove 1, the NSW Wargroove 2 patch, and Windows
Wargroove 2 so a Korean translation can be prepared safely.

**Architecture:** Keep the repository as a lightweight document-and-reference
workspace. Analyze each `config.dat` and `ui.dat` source separately, then
prepare Wargroove 2 from its own Windows structure rather than overwriting it
with the NSW patch.

Analysis findings are recorded continuously in `work/docs/analysis/`, with
confirmed facts, hypotheses, blockers, and next checks kept distinct.

**Tech Stack:** Markdown and Git ignore rules.

**Spec:** `docs/specs/2026-09-26-translation-workspace-design.md`

## Global Constraints

- Do not use a `po/` directory.
- Do not assume every game uses the same source format or translation method.
- Preserve source files and existing translations by default.
- Do not perform automatic full rewrites or start the next work cycle automatically.
- The first setup must be a safe skeleton and must not require real game files.
- Keep credentials, local machine secrets, and external service integration out of the initial setup.

### Task 1: Add minimal project structure and documentation

- [x] Add README and ignore rules.
- [x] Document the reference directory and delayed game-specific setup.

### Task 2: Add AI and design guidance

- [x] Add tool-neutral AI guidance.
- [x] Keep design documents under `docs/`.

### Task 3: Add target-specific source and work structure

- [x] Add immutable `src/Wargroove 1/2.1.x/config/` and
  `src/Wargroove 2/1.2.x/config/` source snapshots.
- [x] Generate readable Wargroove 2 ConfigFile JSON under
  `work/docs/analysis/wargroove2-config-readable/`.
- [x] Add matching editable `work/Wargroove 1/2.1.x/config/` and
  `work/Wargroove 2/1.2.x/config/` directories.
- [x] Add root `tools/` for HALLEYPK, ConfigFile, and build tools, plus
  root `tests/` for regression tests and fixtures.
- [x] Add dated `dist/` release directories.
- [x] Consolidate mutable analysis and review records under `work/docs/`.
- [x] Create the Git-ignored `references/` directory for local materials.

### Task 4: Analyze translation sources

- [x] Identify the `HALLEYPK` container and zlib-compressed index.
- [x] Confirm the NSW patch files are under `romfs/`.
- [x] Confirm the NSW patch has `ko-KR` Wargroove 2 string resources and the
  Windows Wargroove 2 index does not.
- [x] Preserve the extracted Wargroove 1 language resources under
  `references/Nexus/ModPacker-Wargoove-results/` as terminology references.
- [ ] Compare the extracted Wargroove 1 language JSON files.
- [ ] Extract language payloads from the NSW Wargroove 2 patch files.
- [ ] Parse the Windows Wargroove 2 `ui.dat` index and payloads.
- [ ] Determine how to add a Korean string payload to the Windows pack.
- [ ] Repack a copy of `ui.dat` and validate it before any game installation.
- [x] Repack all six `config.dat` and `ui.dat` files into temporary copies and
  validate every indexed payload.
- [x] Add one asset to a Wargroove 2 pack copy and validate the new output.
- [x] Add real Korean string payloads after confirming their runtime
  serialization format.
- [ ] Compare the Windows Wargroove 2 structure and identify safe Korean
  insertion points.
- [ ] Build Wargroove 2 Korean terminology from Wargroove 1 first, using the
  NSW patch and other languages as references.
