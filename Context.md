# Context

## Repository Purpose

This repository supports the AI Engineering Lab Hackathon London 2026. It provides challenge briefs, starter data, setup guidance, and prototype artefacts for a one-day AI-assisted engineering event.

The event is about how AI coding tools change software delivery. It does not require teams to embed live model APIs in their prototypes. Mocked AI capabilities are acceptable when teams can explain what is mocked and what would be needed to productionise it.

## Current Prototype Focus

The active build work has focused on Challenge 2: Unlocking the dark data.

Challenge 2 asks teams to turn messy government guidance, policy, procedural documents, PDFs, Word files, and spreadsheets into structured, findable, machine-usable content. The current prototype implements this as an Obsidian-friendly LLM Wiki:

- Raw Challenge 2 sources remain immutable.
- Generated Markdown notes live under `challenge-2/wiki/`.
- One source note is generated for each raw source document.
- Topic, entity, and map notes provide navigable synthesis.
- JSON and table exports provide machine-readable interfaces.
- Lint output checks coverage, metadata, links, and known challenge flags.

## Data Assumptions

- Challenge starter data is synthetic unless the relevant challenge brief says otherwise.
- Challenge 2 staff-directory names, emails, phone-like values, roles, and identifiers are synthetic fixture data and should not be redacted for the demo.
- Real secrets, credentials, local filesystem paths, and provenance gaps remain review issues.
- Raw files under Challenge 2 source folders should not be edited, renamed, moved, or normalised as part of wiki generation.

## Important Paths

- `README.md`: event overview, challenge list, judging model, and materials.
- `Changelog.md`: dated change history.
- `Context.md`: project context, architecture assumptions, and operating constraints.
- `Progress.md`: current status, validation, blockers, and next steps.
- `AGENTS.md`: repo-wide operating rules and documentation lockstep policy.
- `tools/check_documentation_lockstep.py`: local and CI check that required tracking docs exist and move with meaningful changes.
- `challenge-2/AGENTS.md`: Challenge 2 LLM Wiki operating schema.
- `challenge-2/tools/build_wiki.py`: repeatable Challenge 2 wiki builder.
- `challenge-2/wiki/index.md`: Obsidian knowledge-base entry point.
- `challenge-2/wiki/architecture.md`: plain-English architecture explanation with Mermaid diagrams.
- `challenge-2/wiki/lint-report.md`: generated quality report.
- `challenge-2/wiki/data/source-register.json`: machine-readable source register.

## Documentation Lockstep

Documentation is part of the product. Any meaningful change should update the relevant tracking files:

- `Changelog.md` for what changed.
- `Context.md` for changed assumptions, architecture, or constraints.
- `Progress.md` for changed status, blockers, validation, or next steps.
- `README.md` or challenge briefs for user-facing changes.

This rule is enforced through `AGENTS.md`, `.github/pull_request_template.md`, `tools/check_documentation_lockstep.py`, and the Documentation Lockstep GitHub Actions workflow. The check fails if required tracking files are missing or if meaningful changes omit a tracking-file update.
