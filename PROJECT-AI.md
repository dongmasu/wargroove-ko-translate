# Project AI Guidelines

This document defines project-level guidance for any AI-assisted work.
It is intentionally neutral about vendors, models, editors, agents, and
command-line tools.

## Project Scope

The project targets a Korean translation for the Windows version of Wargroove
2. macOS is not a supported platform for this project. Wargroove 1 has an
official Korean translation and may be used as reference material for
terminology and style.

## Priorities

When instructions conflict, use this order:

1. Safety and protection of user data.
2. Explicit user requests.
3. Repository documentation and configuration.
4. The smallest change that satisfies the request.
5. General engineering conventions.

## Before Changing Files

- Inspect the relevant files, directory structure, and existing documentation.
- Identify the smallest set of files needed for the task.
- Do not assume a game format, translation workflow, or external service.
- Check for uncommitted work before touching files when repository metadata is
  available.
- Never read, expose, or copy credentials, tokens, private keys, certificates,
  or secret configuration.

## Translation Rules

- Preserve the source meaning, context, speaker identity, tone, and intent.
- Follow the applicable game glossary and style rules before inventing new
  terminology.
- Keep placeholders, markup, escape sequences, control codes, and identifiers
  unchanged unless the target format explicitly requires otherwise.
- Preserve line structure, ordering, and required file encoding.
- Keep Korean honorifics, speech levels, names, titles, and self-reference
  consistent with context.
- Do not silently resolve ambiguity. Record a note or mark the item for review.
- Avoid literal translations that sound unnatural when the source context
  supports a clearer Korean expression.

## Wargroove Analysis Order

- Analyze Windows Wargroove 1 before making terminology decisions for
  Wargroove 2.
- Analyze the NSW Wargroove 2 patch separately; do not assume it can overwrite
  the Windows Wargroove 2 files.
- Analyze the Windows Wargroove 2 file structure before preparing any Korean
  insertion or application step.
- Extract English, Japanese, Chinese, and Korean data as separate sources.
- Treat Wargroove 1's official Korean localization as the primary terminology
  reference.
- Use Japanese, especially its similar word order, as a translation reference
  without treating it as authoritative.

## Change Safety

- Preserve source files and existing translations by default.
- Prefer new output files, backups, or reversible changes over in-place writes.
- Do not delete, overwrite, bulk-rewrite, or publish data without an explicit
  request.
- Validation and reporting should be read-only when they are introduced.
- Do not add external services, dependencies, or credentials unless requested
  and documented.

## Workflow

1. Inspect the relevant source and configuration.
2. State assumptions when the request leaves important ambiguity.
3. Make the smallest focused change.
4. Run the narrowest relevant tests or validation commands.
5. Review the diff and check for accidental generated files or secrets.
6. Report changed files, verification results, and any remaining uncertainty.
7. Record meaningful analysis findings continuously in `work/docs/analysis/`.

Analysis notes should distinguish confirmed facts, working hypotheses,
unknowns, blocked actions, and the next verification step. Do not wait until
the end of a long investigation to document the findings.

Platform-specific procedures must be documented separately. Windows game
asset replacement must be tested on Windows, and macOS analysis must not be
assumed to produce Windows-valid game files without verification.

## Repository Boundaries

- Local source material and other references belong under `references/`.
- `references/` is excluded from Git and must not be used for secrets.
- Add game-specific directories or scripts only when the target workflow
  justifies them.
- Design and implementation documents belong under `docs/`.

## Tool Neutrality

Any AI tool may follow this document, but no tool-specific command, role name,
prompt syntax, plugin, or proprietary feature is required. Tool-specific
instructions may supplement this document only when they do not conflict with
these project rules.
