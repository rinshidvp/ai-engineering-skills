---
name: software-design
description: "Turn a spec, BRD, or rough feature request into a solid software design by forcing intermediate artifacts before implementation: problem model, discovery memo, layer stack, candidate decompositions, component contracts, and validation scenarios. Also covers implementing from a design (CONTRACT blocks, DESIGN.md sync) and reviewing designs for quality. Use when designing any non-trivial feature, when implementing from an existing design, or when reviewing design quality."
---

# Designing Features

> Portability: design doc lives at `tasks/YYYY-MM-DD-<slug>.design.md`, promoted to `<module>/DESIGN.md` on implementation. Contracts go as CONTRACT blocks in code. Read `GLOSSARY.md` (for domain names) and `docs/adr/` (for settled architectural decisions) before designing. Phase work can run in subagents (spawn tool per host: `../_shared/hosts.md`). Upstream input: `../discovery/SKILL.md` requirements (R-numbered). Downstream: `../implementation-plan/SKILL.md`.

## Mindset

Your job is complexity management. A good design finds the right boundaries so that each part of the system can *forget* about the rest — not just "doesn't need to know," but actively forgets. The component doesn't exist in its mental model. That's the bar.

The reason you force intermediate artifacts — problem model, discovery memo, layer stack — before naming any component is that jumping straight from requirements to code produces designs shaped by whatever the author thought of first, not by the actual forces in the problem. The artifacts slow you down just enough to see the natural seams before you cut.

A design is the contracts: the guarantees, expectations, and refusals that let everything else stop thinking about what's behind the interface. If the contracts are explicit and findable, a new session can work on any component without understanding the whole system.

## What are you doing?

This skill serves three phases. Find yours:

**Creating a design** — you have a spec, BRD, or feature request and need to produce a design before implementation. → Read `references/creating.md`

**Implementing with a design** — a design exists (DESIGN.md, tasks/design.md, or contracts in a sprint context). You're writing code and need to document contracts, keep design artifacts in sync, and respect boundaries. → Read `references/implementing.md`

**Reviewing a design** — you're checking whether a design is sound before implementation, or whether the code matches the design after implementation. → Read `references/reviewing.md`

## Component Contract Fields (write in code CONTRACT blocks)

For every component, specify:
- **GUARANTEES** — what callers can rely on (specific, testable). Bad: "handles errors gracefully". Good: "returns `TimeoutError` after `max_wait_ms` with no persisted side effects"
- **EXPECTS** — preconditions on inputs, state, and calling order
- **FAILURE BEHAVIOR** — deterministic behavior for each important failure mode
- **DOES NOT** — explicit refusals that keep the boundary hard
- **KNOWN LIMITATIONS** — work that belongs here but deliberately not handled yet
- **EMITS** (optional) — logs, metrics, events, traces callers/operators should expect

See `references/design-smells.md` for coupling smells to avoid.

## Heuristics

- Separate essential complexity (business problem) from accidental complexity (implementation mess)
- Push I/O and external wonkiness below the domain layer
- Single responsibility at every level — module, package, method
- Design to interfaces — callers and tests cross the same seam; if you want to test *past* the interface, the module is the wrong shape
- Prefer **deep modules** (small interface, lots of hidden behavior → leverage for callers, locality for maintainers) over shallow pass-through wrappers
- **The deletion test:** imagine deleting a module. If complexity vanishes, it was a pass-through; if complexity reappears across N callers, it earns its keep
- **Real seams only:** one adapter = hypothetical seam; two adapters = real seam. Don't add indirection unless something actually varies across it
- **Design interfaces for testability:** (1) accept dependencies instead of creating them inside, (2) return results instead of mutating hidden state, (3) keep the surface area small
- Focused, composable modules beat monoliths that "do everything"
- Make illegal states unrepresentable where possible
- If core logic needs mocks to test basic decisions, the seam is in the wrong place
- If a likely change cuts across many modules, locality is broken and the seam is probably wrong
- If a layer cannot say what complexity it absorbs, it should not exist

## Output Shape

When asked to produce a design, present in this order:

1. normalized problem model
2. discovery memo
3. proposed layer stack
4. candidate decompositions (with known patterns considered)
5. comparison on engineering quality vs simplicity
6. recommendation — chosen design with rationale and trade-offs
7. component contracts
8. assumptions
9. validation and failure analysis
10. open questions

Do not skip directly to component lists. Do not skip the comparison.