---
name: code-quality
description: Design-level code quality - pragmatic architecture review, behavior-preserving simplification, single-responsibility (SRP) redesign, and "is this feature actually complete?" checks. Use after finishing a feature, when a component seems to do too much, when asked for an architecture or SRP review, or to check implementation completeness.
---

# Code Quality

The goal is obvious, maintainable code that ships: not clever code, and not
ivory-tower purity. This skill has four modes. Pick the one that matches the
request and read its reference file; you rarely need more than one.

| Mode | Use when | Read |
|------|----------|------|
| **Pragmatic review** | A feature is built and needs an independent design-level review with a SHIP / SHIP-WITH-FIXES / REWORK verdict | `references/review.md` |
| **Simplification** | Changed code works but is harder to read than it needs to be; strictly behavior-preserving | `references/simplify.md` |
| **SRP redesign** | A component mixes several responsibilities and you want a clean-slate decomposition | `references/srp.md` |
| **Completeness check** | You've finished a feature and want a fresh agent to find what you forgot | `references/completeness.md` |

## Principles shared by all modes

1. **Clarity over cleverness.** Code should be easy to reason about.
2. **Simplicity over flexibility.** Solve today's problem; refactor when a real
   second case appears.
3. **Every layer earns its place.** If you can't say what complexity a file,
   interface or layer absorbs, it shouldn't exist.
4. **Reviews are independent.** The author of the code shares its blind spots,
   so reviews and completeness checks go to a separate agent with fresh context.
   Point it at file paths; don't paste code.

## Related

- Coupling smells to look for: `../software-design/references/design-smells.md`
- Test discipline for the test pass: `../writing-unit-tests/SKILL.md`
- Review → fix → verify loop with a two-pass cap: `../refine-loop/SKILL.md`
- On Claude Code, the built-in `/code-review` (bug hunt on a diff) and
  `/simplify` (quick cleanup) cover lighter versions of the review and
  simplification modes. See `../_shared/hosts.md`.
