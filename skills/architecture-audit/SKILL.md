---
name: architecture-audit
description: Scan an existing codebase for shallow modules, poor locality, and untestable seams, present deepening opportunities as a visual HTML before/after report, then grill through the chosen refactor. Use when a repo feels messy or hard to change, after rapid AI coding, or for periodic architecture cleanup.
---

# Architecture Audit

Fight codebase slop proactively. Surface architectural friction in an existing
repo and propose **deepening opportunities** — refactors that merge shallow,
scattered wrappers into **deep modules** (small interface, hidden complexity,
clean seam, testable from the outside).

## Shared Vocabulary

Use these terms consistently in every finding (avoid drifting into vague words
like "component", "service", or "helper"):

- **Module:** anything with an interface and an implementation (function, class,
  file cluster, or slice).
- **Interface:** everything a caller or test must know to use the module
  (signature, invariants, error modes, ordering).
- **Depth:** leverage at the interface — lots of behavior hidden behind a small,
  simple surface. Opposite of **shallow** (interface nearly as complex as the
  body).
- **Seam:** the place where an interface lives and behavior can be swapped
  (e.g. real DB vs. in-memory fake). *One adapter = hypothetical seam; two
  adapters = real seam.*
- **Locality:** related logic, bugs, and tests live together in one place
  rather than scattered across many files.
- **Deletion test:** imagine deleting the module. If complexity vanishes, it
  was a useless pass-through; if complexity reappears across callers, it earns
  its keep.

## Process

### 1. Scope by Hotspots (YAGNI)

Refactoring code you never touch wastes time. Decide *where* to scan first:

- If the user named a folder, feature, or pain point, focus there.
- Otherwise, inspect recent commit history (`git log --oneline -n 40 --stat`)
  to find **hotspots** — files and areas that keep changing. Focus there first.

Read `GLOSSARY.md` (for domain names) and `docs/adr/` (so you don't
re-suggest things already ruled out) before scanning.

### 2. Explore in a Fresh Subagent

Dispatch a fresh-context explorer subagent on the fast tier (see
`../_shared/hosts.md`) so raw file reading does not bloat the main session.
Have it look organically for real friction:

- Understanding one domain concept requires bouncing across 4+ tiny files.
- Shallow modules that fail the **deletion test** (just passing args through).
- Duplicated logic across sibling modules that should share one deep module.
- Hard-to-test code (creates dependencies internally instead of accepting them,
  or mutates hidden state instead of returning results).
- Pure helpers extracted only to make unit tests easy while real bugs hide in
  the untested glue around them.

### 3. Present a Visual HTML Before/After Report

Write a self-contained HTML file to the OS temp directory (`%TEMP%` on Windows,
`$TMPDIR` or `/tmp` on macOS/Linux) as
`<tmpdir>/architecture-audit-<timestamp>.html` so nothing pollutes the repo.
Open it in the user's browser and print the file path.

Keep the report scannable and visual (Tailwind CDN + Mermaid CDN or clean
inline SVG/CSS diagrams):

For each candidate, render a card with:
- **Files:** involved paths
- **Problem:** plain-English explanation of the friction
- **Solution:** how deepening fixes it
- **Benefits:** concrete gains in **locality**, **leverage**, and **testability**
- **Before / After diagram:** side-by-side visual showing shallow/scattered vs.
  deep module
- **Strength badge:** `Strong` | `Worth exploring` | `Speculative`
- **ADR warning (only if relevant):** if a candidate contradicts an existing
  ADR *and* the friction is real enough to revisit it, flag it explicitly.

End with a **Top Recommendation** naming which single candidate to tackle first
and why. Use the project's `GLOSSARY.md` domain names throughout.

Do **not** write code or propose final interfaces yet. Ask the user:
**"Which of these would you like to explore?"**

### 4. Grill & Update Docs Before Refactoring

Once the user picks a candidate:
- Hand off to `../discovery/SKILL.md` (Grill mode) to settle constraints,
  seams, and which tests survive — updating `GLOSSARY.md` inline if a new
  domain concept is named.
- If the user **rejects** a candidate for a lasting, non-obvious reason, offer
  a short ADR in `docs/adr/NNNN-slug.md` (*"Want me to record this as an ADR so
  future audits don't re-suggest it?"*).
- Once aligned, move to `../software-design/SKILL.md` or
  `../implementation-plan/SKILL.md` to execute safely.
