# Pragmatic Review

Evaluate code and design decisions against pragmatic principles. The goal: **obvious, maintainable code that ships** — not clever code or ivory-tower purity.

## Core Values (Priority Order)

1. **Clarity over cleverness** — Code should be easy to reason about
2. **Shipping over perfection** — But shipping maintainable work, not hacks
3. **Simplicity over flexibility** — Solve today's problems, refactor when needed
4. **Obviousness over abstraction** — Design feels natural and matches the problem's shape
5. **Domain-focused over implementation-leaking** — Abstractions describe **what**, not **how**
6. **Real gains over ceremony** — Every file, interface, and layer must justify its existence

## The Design "Click" Test

Does this design click?
- Feels obvious, natural, easy to explain
- Matches the problem's natural shape
- Someone could understand it in 6 months without you
- Changes are localized and predictable
- Tests don't require heroic setup

If NO — either too clever, too scattered, or too coupled.

## Invoking a Review

Code review is done by a separate agent with fresh context rather than inline, because the author of the code shares its blind spots. The reviewer reads the design, code quality, and test skills as its methodology.

Spawn the `code-reviewer` agent that `install.ps1` installs on every host (how to spawn it on yours: `../../_shared/hosts.md`). If your host has no subagents, do the passes inline in a fresh context window.

Brief it with:
- What files changed and why
- Any design context (decisions, constraints, rejected alternatives)
- Specific concerns you want checked

The reviewer runs three passes (design, code, tests) and reports findings with a `SHIP` / `SHIP-WITH-FIXES` / `REWORK` verdict. The full review protocol is in the agent's prompt (`agents/code-reviewer/body.md` in the dev-skills repo).

## Quick Reference

| Question | Answer |
|---|---|
| Should I split this class? | No if "lots of related ops" or creates <20 line files. Yes if doing unrelated things. |
| Should I create an interface? | No if "just in case". Yes if 2+ implementations exist NOW or callers shouldn't know the implementation. |
| Too many files/layers? | Ask: what does each layer ADD, not just delegate? "More proper" → remove. "Separates concerns" → keep. |
| Doing too much? | Can't explain in one sentence → split. Can't share data across methods → split. Lots of cohesive code → keep. |
| Do callers know too much? | If callers import implementation types (Sqlite*, Redis*, Http*), the abstraction is missing. Flag it. |

**Swap Test:** If I need to change an implementation detail (database, external service), how many files do I touch? If more than one module → the implementation leaked through the boundary.
