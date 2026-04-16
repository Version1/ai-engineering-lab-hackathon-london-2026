# Changelog

All notable changes to this repository are tracked here.

This file follows the spirit of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/): dated entries, human-readable summaries, and clear categories for additions, changes, fixes, removals, security notes, and documentation updates.

## Unreleased

### Added

- Added repo-wide tracking files: `Changelog.md`, `Context.md`, and `Progress.md`.
- Added repo-wide operating rules in `AGENTS.md` requiring documentation updates in lockstep with implementation changes.
- Added a GitHub pull request template with explicit documentation lockstep checks.
- Added `tools/check_documentation_lockstep.py` and a GitHub Actions workflow to enforce tracking-file updates on pull requests.
- Added `challenge-2/wiki/evaluation-benchmark.md` with 100 source-backed questions, gold answers, per-question rubrics, and a 500-point summative scoring regime for Challenge 2 wiki evaluation.
- Added a Challenge 2 wiki evaluation harness under `challenge-2/evaluation/` and `challenge-2/tools/run_wiki_eval.py` for Codex, Gemini CLI, and Claude Code prompt runs.
- Added `challenge-2/tools/wiki_eval_mcp.py`, a stdio MCP-compatible audit layer for controlled wiki search/read, answer recording, and DSAP-shaped audit pack finalisation.
- Added `challenge-2/tools/summarise_wiki_eval.py` to turn completed scoring sheets into leaderboard JSON and Markdown.

### Fixed

- Updated the Challenge 2 architecture Mermaid labels from `1.`, `2.`, etc. to `Step 1:`, `Step 2:`, etc. so Obsidian does not render them as unsupported Markdown lists.
- Fixed the documentation lockstep check so it fails if required tracking files are deleted, even when their deleted paths appear in the diff.

### Documentation

- Linked the new tracking files from `README.md`.
- Linked the Challenge 2 benchmark into the wiki index and documented the evaluation harness in the Challenge 2 brief and README.

## 2026-04-16

### Added

- Added the Challenge 2 Obsidian knowledge base under `challenge-2/wiki/`.
- Added `challenge-2/tools/build_wiki.py` to generate source notes, topic pages, entity pages, maps of content, table exports, source register data, architecture documentation, and lint output.
- Added Challenge 2 Obsidian vault configuration under `challenge-2/.obsidian/`.
- Added `challenge-2/AGENTS.md` with operating rules for the generated LLM Wiki.
- Added `challenge-2/wiki/architecture.md` with Mermaid diagrams and a glossary explaining the knowledge-base architecture.
- Added GitHub Copilot custom instructions for Challenge 2 synthetic fixture data.

### Changed

- Treated `challenge-2/` as the Obsidian vault root so raw source files, generated notes, and links live together.
- Preserved synthetic staff-directory fixture data while marking it as synthetic and not real personal data.
- Generated source notes for all 43 Challenge 2 documents.

### Fixed

- Fixed malformed generated Markdown links caused by rewriting document IDs inside existing links.
- Fixed `/guidance/DOC-*` pseudo-links by rewriting them to relative source-note links.
- Removed ExifTool local-environment fields from generated raw metadata and source-register output.
- Fixed Social Fund version extraction to capture `March 2018`.
- Added a corrected HMT Green Book link while preserving the raw extracted PDF text.
- Fixed singular wording for topic pages with exactly one source document.

### Validation

- Verified the Challenge 2 strict build: `43 sources, 81 notes, 0 lint issues`.
- Resolved all fork-local PR review threads for the Challenge 2 work.
