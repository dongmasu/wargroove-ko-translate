# Translation Batch 007: Full Quality Review Scope

Date: 2026-09-27

## Purpose

This report freezes the first target list for a complete Korean translation
quality review. It is a review-scope document only. No translation resource
is changed in this stage.

## Baseline

- Target: Windows Wargroove 2 `v1.2.12`, build `#45031`
- Korean resources: 24
- Generated entries: 15,198
- Source/reference priority: Wargroove 1 Korean, NSW Korean, English,
  Japanese, then Simplified/Traditional Chinese
- Review roles: reviewer, approver, editor, verifier, publisher
- Required flow: scope freeze -> read-only review -> report -> approval ->
  scoped edit -> independent verification -> package/test

## Candidate Findings

The existing coverage audit identifies the following candidate classes:

| Candidate class | Count | Initial treatment |
| --- | ---: | --- |
| Missing English keys | 0 | No target unless a new source comparison finds one |
| Placeholder mismatches | 0 | Recheck only when editing the same key |
| Empty Korean values | 22 | Review whether source/runtime semantics justify retention |
| English/Korean identical values | 335 | Classify as intentional, untranslated, or ambiguous |
| Markup tag differences | 310 | Compare meaning, tag scope, and rendered behavior |
| Corrupted-source `???` campaign keys | 4 | Review against all reference languages and runtime context |

The counts are candidate counts, not confirmed errors.

## Priority Order

### P0: Known unresolved or potentially harmful

- Four corrupted campaign-air keys represented by `???`.
- All 22 empty Korean values.
- The 310 markup-difference keys, beginning with campaign dialogue and
  objectives where tag scope can change delivery or meaning.
- The five Faahri Tutorial 4 exception keys recorded in
  `translation-exceptions.tsv`, including the `Swordsman`/`Duelist`
  correction.

### P1: Semantic and naturalness review

- Remaining campaign-air strings after the A1M1 opening pass.
- Campaign-earth, campaign-sea, and campaign-final dialogue, objectives, map
  names, and cutscene text.
- Campaign tutorial instructions and unit/action references.
- Conquest event text and choice labels.
- Codex commander, unit, lore, and structure descriptions.

### P2: Consistency and low-priority review

- The 335 English/Korean-identical values after intentional technical values
  are excluded.
- UI labels, settings, credits, language names, numeric values, and developer
  or audio identifiers that remain ambiguous after classification.
- Gallery, secret, groove, and append resources.

## Required Review Record

For every proposed change, the reviewer must record:

- resource file and stable key;
- English source and current Korean value;
- Japanese/Chinese evidence when useful;
- Wargroove 1 and NSW terminology references;
- issue type: terminology, continuity, meaning, naturalness, markup, UI, or
  source defect;
- proposed Korean revision or explicit defer decision;
- confidence and affected resources;
- status: `수정`, `문제 없음`, or `계속 보류`.

## Stage Boundary

The reviewer must not modify `work/Wargroove 2/1.2.x/config/` during this
scope stage. After the first review batch is approved, the editor may change
only the approved keys. The verifier must compare the resulting diff against
this report and rerun the resource and package checks.

## Known Documentation Gap

`translation-progress.md` describes the campaign review as complete, while
`batch-003-campaign-air-naturalness.md` explicitly leaves additional campaign
air and tutorial review as the next scope. Until those resources are reviewed
and recorded, the project must treat full translation quality review as
incomplete.
