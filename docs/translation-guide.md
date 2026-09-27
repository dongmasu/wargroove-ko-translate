# Wargroove Korean Translation Guide

This document is the practical guide for translating Wargroove resources.
The glossary defines recurring terms; this guide defines how to translate
strings when terminology, context, or the game implementation creates an
exception.

## Source Priority

Use sources in this order:

1. Wargroove 1 official Korean localization
2. NSW Wargroove 2 Korean translation
3. Wargroove 2 English source
4. Wargroove 2 Japanese source
5. Wargroove 2 Simplified and Traditional Chinese sources

This is a decision order, not a blind replacement rule. Wargroove 2 may
reuse a Wargroove 1 word in a different faction or context. Prefer the
meaning that matches the current resource and gameplay.

## Core Rules

### Names and Terms

- Keep character, faction, place, unit, ability, and item names consistent
  with the versioned glossary.
- Prefer Wargroove 1 Korean terms when the same entity and meaning continue
  into Wargroove 2.
- Use the NSW translation as a starting point for Wargroove 2-only content,
  then verify it against English context.
- Do not translate a proper name globally without checking every affected
  key. A word may be a name in one resource and a common noun in another.
- Record intentional departures from Wargroove 1 or NSW in the versioned
  exception list.

### Context

- Check the speaker, faction, unit type, mission, and gameplay state before
  choosing a term.
- Distinguish a generic source label from a faction-specific unit name.
  For example, `Swordsman` is Cherrystone's unit name, while Faahri's
  corresponding soldier is `Duelist`.
- Treat tutorial text, codex text, UI labels, and dialogue as separate
  contexts even when they contain the same English word.
- Use Japanese to check clause order and implied subjects, not as the sole
  authority for meaning.
- Use Chinese to cross-check whether a short English expression carries an
  omitted subject, object, or modifier.

### Korean Style

- Prefer clear, concise Korean for UI and tutorial instructions.
- Preserve character voice, honorific level, emotional tone, and intentional
  repetition in dialogue.
- Use established Korean game terminology rather than literal translation
  when it improves clarity and does not break continuity.
- Keep names and titles readable in compact UI areas. Do not add explanatory
  text to a unit name unless the source contains it.
- Use Korean punctuation and spacing naturally, but do not alter control
  tokens or markup.

### Technical Preservation

- Never change resource keys.
- Preserve placeholders, markup, color tags, timing tags, escape sequences,
  and intentional line breaks.
- Do not replace a source term inside a control token or identifier.
- Keep JSON valid and preserve the expected resource file structure.
- Edit extracted copies under `work/`, never files under `references/` or
  immutable files under `src/`.

## Exception Handling

An exception is required when any of the following applies:

- Wargroove 1 and NSW use different terms for the same Wargroove 2 entity.
- The same English word refers to different entities or factions.
- A tutorial refers to a unit that is not available in the current mission.
- A source string is reused in a different gameplay context.
- Literal translation conflicts with the established Korean name.
- A UI constraint requires a shorter or structurally different phrase.
- A source inconsistency must be corrected for the Korean version to be
  understandable or playable.

For every exception:

1. Record the source key and the affected resource.
2. Identify the English, Japanese, and Chinese evidence when useful.
3. Explain why the normal glossary rule does not apply.
4. Record the chosen Korean expression and its scope.
5. Add the case to the versioned exception list.
6. Add a review report when the change affects multiple resources or gameplay
   instructions.

The exception list is not a blind replacement list. Each row applies only to
the listed keys or explicitly stated scope.

## Review Checklist

- Is the entity or faction correctly identified?
- Does the Korean term match the versioned glossary?
- If it differs, is the exception recorded?
- Does the string fit the speaker and gameplay context?
- Are placeholders, markup, and line breaks unchanged?
- Does the tutorial describe an actually available unit or action?
- Does the text fit the target UI and selected font?
- Has the changed key been included in the review report?

## Records

- Common workflow: `docs/translation-process.md`
- Versioned terminology: `work/<game>/<version>/wg2-terminology.tsv`
- Versioned exceptions: `work/<game>/<version>/translation-exceptions.tsv`
- Batch evidence and decisions: `work/docs/review/`
