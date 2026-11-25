---
name: retro
description: Conduct a retrospective on a finished coding session or PR to permanently improve the repo's environment (deterministic checks, CODING_STANDARDS.md, navigation pointers, and pruning AGENTS.md bloat). Use after merging a PR, finishing a feature, or when the agent repeated a preventable mistake.
---

# Retrospective

Never fix the same class of mistake twice. Inspect a finished session or PR and
propose concrete upgrades to the **environment** so future agent runs perform
better automatically.

## Core Principle: Determinism First, Review Second, `AGENTS.md` Last

- **Mechanical mistakes** (banned APIs, `any` types, import rules, formatting,
  file placement) → enforce with a **deterministic check** (linter rule,
  TypeScript strict config, pre-commit hook, or CI check). Zero tokens, 100%
  reliable.
- **Judgment calls** (cross-file consistency, design patterns no linter can
  check) → add a crisp rule to `CODING_STANDARDS.md`, which `code-reviewer`
  enforces (the reviewer has low context pressure; the builder has high context
  pressure).
- **`CLAUDE.md` / `AGENTS.md`** → keep tiny! Use only for short **navigation
  pointers** to other docs (`GLOSSARY.md`, `CODING_STANDARDS.md`, `docs/adr/`).

## Steps

1. **Read the session or PR evidence:** Use the current session (or the PR /
   recent commits / review comments the user points to). Also inspect the
   repo's existing check scripts (`package.json`, CI workflows, linter config).
2. **Scan these 6 improvement categories:**
   - **Automated checks (highest priority):** Could a linter, strict type check,
     test, pre-commit hook, or CI job have caught the mistake? If the repo has
     *no* lint/typecheck/test guardrail wired up, flag that as a top finding.
   - **Coding standards:** Did `code-reviewer` miss a judgment-call issue that
     belongs in `CODING_STANDARDS.md`? (Default to an automated check over a
     prose rule whenever possible.)
   - **Navigation:** Did the agent burn turns hunting for files or hidden
     dependencies? Add a 1-line navigation pointer in `AGENTS.md` / `CLAUDE.md`.
   - **Bloat & no-ops:** Are `AGENTS.md`, `CODING_STANDARDS.md`, or skills
     carrying stale rules or instructions the model already obeys by default?
     Delete no-ops; state rules positively (*"write 1-line comments"* instead
     of *"don't write long comments"*).
   - **Tool & context economy:** Did the agent run expensive broad commands
     instead of targeted ones, or bloat context when a subagent/pointer would
     have kept it in the Smart Zone?
   - **Information access:** Was a crucial signal missing (dev server logs,
     schema dump, read-only CLI)?
3. **Present findings ranked by impact:** For each candidate, state the
   mistake it prevents, the exact file/check to add or edit, and whether it is
   **deterministic** or a **judgment rule**. Wait for the user to pick which
   ones to apply.
