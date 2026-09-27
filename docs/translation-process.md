# Wargroove 2 Korean Translation Process

## Goal

Create a Korean translation for the Windows version of Wargroove 2 while
preserving terminology and continuity across Wargroove 1, the NSW Wargroove 2
patch, and new Wargroove 2 content.

The NSW patch is a translation reference, not a file replacement source.
Windows Wargroove 2 remains the target structure and base package.

This role model is adapted from the local
`/Users/donghyki/wesnoth-ko-translate` project, especially its
`PROJECT-AI.md`, `work/1.18.x/TRANSLATION-RULES.md`, and
`docs/superpowers/specs/2026-09-25-review-edit-role-separation-design.md`.
Wargroove replaces Wesnoth's PO/MO-specific checks with resource-key,
payload, package, and Windows runtime checks.

## Roles and Approval Flow

The workflow follows the role separation used by the
`wesnoth-ko-translate` project. One person or AI may perform multiple roles,
but the roles must not be collapsed into one unreviewed pass.

```text
scope freeze
  -> read-only review
  -> review report
  -> approval
  -> scoped edit
  -> independent verification
  -> package/test
  -> release report
```

### Reviewer

The reviewer reads source resources, reference languages, the glossary, and
existing Korean translations without modifying translation assets. The
reviewer records:

- resource key and source language;
- current Korean translation, if any;
- proposed translation or issue;
- Wargroove 1 and NSW references;
- English/Japanese/Chinese evidence;
- confidence and affected resources;
- status: `수정`, `문제 없음`, or `계속 보류`.

Review reports belong under `work/docs/review/` and are the scope for the next
stage.

### Approver

The approver accepts exact review items or returns them for more evidence.
Approval must identify the resource keys or glossary rows that may change.
Uncertain terminology, especially names and places, remains blocked rather
than being silently decided.

### Editor

The editor changes only approved resource keys and glossary rows. The editor
must:

- preserve entries outside the approved scope;
- update the glossary before applying dependent translations;
- avoid global replacement unless every affected key is listed;
- keep payload format, placeholders, markup, and control codes unchanged;
- stop if the output changes more resources than approved.

### Verifier

The verifier independently checks the edit against the review report. Checks
include:

- terminology and continuity;
- English meaning and Japanese sentence structure;
- Chinese semantic cross-check;
- placeholders, markup, escape sequences, and line structure;
- changed key count and diff scope;
- `halleypk.py` parsing and payload verification;
- successful packing and reopening of the generated package.

Passing binary or structural checks does not by itself prove that the Korean
translation is semantically correct.

### Publisher

The publisher handles only verified output. The publisher creates the final
package, records source and output hashes, records the target Windows game
build, and writes the release report. The publisher must not revise
translations or rerun broad editing tools.

### Stage Boundaries

| Stage | Allowed writes | Required output |
| --- | --- | --- |
| Scope freeze | None | target files, source versions, baseline hashes |
| Review | `work/docs/review/` only | candidate findings and evidence |
| Approval | approval record | exact keys and glossary rows |
| Edit | approved translation work files | scoped translation diff |
| Verify | verification reports only | semantic and technical results |
| Package | new files under `dist/<game>/<version>/<yyyymmdd>/` | generated `config.dat`/`ui.dat` |
| Release | explicit release artifacts | hashes, notes, known issues |

Stop instead of continuing when the scope is ambiguous, an existing
translation may already be correct, evidence is insufficient, or a tool
changes more resources than the approved scope.

## Reference Priority

Use references in this order:

1. Wargroove 1 official Korean localization
2. Existing Korean translations in the NSW Wargroove 2 patch
3. Wargroove 2 English source, for exact meaning and context
4. Wargroove 2 Japanese source, especially for sentence structure and nuance
5. Wargroove 2 Chinese source, for semantic cross-checking and terminology

The priority is not absolute. When a Wargroove 2 context differs from
Wargroove 1, record the difference and prefer the contextually correct
translation.

## Phase 0: Preserve Sources

- Never edit files under `references/`.
- Work only on extracted copies under `work/`.
- Record source file names, extraction date, and source language.
- Keep generated packages separate from source packages.

## Phase 1: Extract and Map

1. Parse Windows Wargroove 1 `config.dat` and `ui.dat`.
2. Parse NSW Wargroove 2 `config.dat` and `ui.dat`.
3. Parse Windows Wargroove 2 `config.dat` and `ui.dat`.
4. Extract English, Japanese, Chinese, and Korean resources separately.
5. Match resources by logical path and identify:
   - same resource in all versions;
   - Wargroove 2-only resources;
   - NSW Korean resources missing from Windows Wargroove 2;
   - resources with changed key sets or structure.

The first output of this phase is a resource map, not a translation draft.

## Phase 2: Build the Glossary

Create a glossary row for each continuity-sensitive term:

| Field | Description |
| --- | --- |
| `key` | Stable source/resource identifier |
| `category` | Character, place, faction, unit, ability, item, UI, etc. |
| `en` | English source |
| `ja` | Japanese reference |
| `zh-Hans` / `zh-Hant` | Chinese references |
| `ko-wg1` | Wargroove 1 official Korean |
| `ko-nsw` | NSW Wargroove 2 Korean |
| `ko-proposed` | Proposed Windows Wargroove 2 Korean |
| `status` | `unreviewed`, `draft`, `review`, `approved`, or `blocked` |
| `notes` | Context, conflict, or decision record |

At minimum, glossary coverage must include:

- character names and titles;
- place names;
- factions and organizations;
- units and commanders;
- grooves, abilities, weapons, and items;
- campaign and codex terminology;
- recurring UI actions and status terms.

When Wargroove 1 and NSW terminology conflict, do not silently choose one.
Keep both references, explain the decision, and mark the proposed term for
review.

Glossary changes follow the same review flow as translation changes. A
glossary row is not an instruction for blind global replacement; its affected
resource keys must be reviewed before applying it.

Practical translation rules and context exceptions are maintained separately
in `docs/translation-guide.md`. Version-specific exceptions belong in
`work/<game>/<version>/translation-exceptions.tsv` and must identify their
affected keys.

## Phase 3: Translate by Context

Translate in this order:

1. Shared names and terminology from the glossary
2. UI labels and short system messages
3. Unit, ability, item, and codex descriptions
4. Campaign objectives and tutorials
5. Character dialogue and narrative text
6. Developer, debug, and low-priority text

For each string:

- preserve the source key;
- preserve placeholders, markup, escape sequences, and control codes;
- preserve gender, number, speaker, honorific, and formality context;
- use Japanese to check clause order, not as the sole semantic authority;
- use Chinese to catch omitted or ambiguous meaning;
- record uncertain strings instead of guessing silently.

## Phase 4: Review

Review in separate passes:

1. **Terminology review:** names and recurring terms are consistent.
2. **Continuity review:** Wargroove 1 and NSW references are respected.
3. **Meaning review:** Korean matches the English context.
4. **Naturalness review:** Korean reads naturally in game context.
5. **Placeholder review:** tokens, markup, and line structure are unchanged.
6. **UI review:** text fits the intended UI space and font.
7. **Technical review:** encoding and runtime resource format are valid.

Every non-approved string remains visible in the review output. Translation
status is tracked per resource, not only per language.

Work is processed in reviewable batches, preferably by resource family or
story/UI area. After a batch, record changed keys, unchanged-but-reviewed
keys, deferred keys, glossary impact, and validation results before starting
the next batch.

## Phase 5: Prepare Windows Assets

- Use Windows Wargroove 2 `config.dat` and `ui.dat` as the base.
- Add Korean resources with `halleypk.py add`.
- Replace or add font assets only after confirming the font payload format.
- Final font decision: start from the untouched Windows Wargroove 2 UI and
  replace only `Noto Serif` with a Google Noto Serif Korean Regular-derived
  single-channel SDF asset. Keep `Sitka Text Bold Italic` and all other font
  assets unchanged.
- Reason for replacement: the original `Noto Serif` contains only 51 Hangul
  syllables, so the direct `Sitka Text Bold Italic -> Noto Serif` fallback
  can show missing glyphs in skill and groove-effect text such as
  `송 사이클론`.
- Final Noto Serif conversion settings are `pixel-size=42`,
  `render-scale=1`, `atlas-width=4096`, `padding=2`, `sdf-radius=4`,
  `sdf-threshold=1`, and `antialias=on`; do not use `--bitmap`.
- The complete command, character-set source, atlas dimensions, payload
  sizes, package hash, and runtime test path are recorded in
  `docs/ui-dat-analysis.md` under “Final Noto Serif Korean replacement
  decision”.
- Repack into new files under `work/`; never overwrite `references/`.
- Keep a manifest of added, replaced, and unchanged resources.

The NSW package must not be copied wholesale into Windows Wargroove 2.
Resource differences must be resolved at the asset and index level.

## Phase 6: Validate

### Automated validation

- Reopen each generated pack with `halleypk.py`.
- Verify expected asset names and types.
- Verify payload sizes and hashes.
- Check that all required Korean resources exist.
- Check that no source language resource was unintentionally removed.
- Check placeholders and control codes against the source.

### Windows game validation

- Test from a clean copy of the Windows game.
- Apply only the generated test package or copied assets.
- Check title/menu, campaign, codex, unit information, dialogue, and settings.
- Check font fallback and Korean glyph rendering.
- Record crashes, missing strings, clipping, and fallback-to-English cases.
- Keep the tested game build and package hash in the test record.

The technical validation baseline for a translation batch is:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tools/halleypk.py list <generated-pack.dat>
python3 tools/halleypk.py pack <generated-pack.dat> <verification-copy.dat>
```

The exact commands and generated paths must be recorded in the batch report.

## Phase 7: Release Candidate

A translation build is a candidate only when:

- all continuity-sensitive glossary terms are approved;
- all targeted Korean resources are present;
- automated package validation passes;
- Windows smoke testing passes;
- unresolved strings and known limitations are documented;
- the output package and source manifest are reproducible.

## Working Status

The current target environment is recorded in
`docs/test-environment.md`:

- Windows Wargroove `v2.1.7`, build `#20187`;
- Windows Wargroove 2 `v1.2.12`, build `#45031`;
- NSW Wargroove 2 version unknown because the game is not owned.

ModPacker 1.6.2 analysis found a conditional AES/CBC payload processing path.
That behavior is now implemented and validated in `tools/halleypk.py`;
details are recorded in `docs/modpacker-analysis.md`.

The Windows WG2 `config.dat` structure and the 24 Korean string resources
required for direct replacement are recorded in
`docs/config-dat-structure.md`. Windows testing confirmed that the
generated Korean pack renders Hangul successfully.

Font conversion is documented in `docs/ui-dat-analysis.md`. The final Noto
Serif Korean SDF conversion and `ui.dat` repack passed automated validation
and was confirmed to apply in Windows Wargroove 2. Final runtime checks should
still be repeated after future font or game-version changes.

The project currently has completed:

- extraction and index mapping for all six `config.dat`/`ui.dat` files;
- pack and add validation on copies;
- initial language resource counts and font resource mapping.
- Halley ConfigFile v3 LZ4 decode/encode support for NSW string resources;
- merged NSW English, Japanese, Simplified Chinese, and Korean JSON resources;
- first terminology batch generated as 24 direct-replacement Korean resources
  with 15,198 string keys;
- format-token validation for approved terminology edits;
- terminology batch 001 with Wargroove 1/NSW conflicts either resolved by
  context decisions or retained in the review record;
- final AES `config.dat` generation and full payload decode verification;

The current translation artifacts are:

- `work/Wargroove 2/1.2.x/wg2-terminology.tsv`
- `work/docs/review/batch-001-terminology.md`
- `work/Wargroove 2/1.2.x/config/translation-draft.json`

The current source is a reproducible translation candidate, not yet a release.
The remaining release gate is the Windows runtime smoke test of the exact
final direct-replacement package. Deferred blank, audio-cue, developer-only,
and corrupted-looking internal keys remain documented in
`work/docs/review/batch-004-missing-keys.md`.
