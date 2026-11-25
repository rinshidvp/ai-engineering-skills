# Wave Planning

## Two Trees, Not One

Plan waves by **testability order**, not just compilation order. A function can compile in wave 1 but only be meaningfully tested in wave 3 when its collaborators exist. If you can't validate a brick without 3 other unbuilt bricks, it doesn't belong in the current wave — no matter how simple the code.

## Brick Layers

- **Leaf** — no unbuilt dependencies, testable now → wave 1
- **Mid-tree** — depends on leaves, testable once leaves pass
- **Canopy** — integration/wiring, testable only when both sides exist

Standard dependency types:
- Foundation (models, types, shared utils) → no dependencies
- Implementation → depends on foundations it uses
- Integration/wiring → depends on components it connects
- Test/verification → depends on code it tests
- No circular dependencies — a cycle means neither brick can prove it works without the other already working, which deadlocks wave planning

## Bad vs Good Wave Plan

**Bad:** Wave 1 builds models + service + handler + router. Everything compiles. Nothing is testable until all four exist. Bugs from wave 1 compound silently into wave 4.

**Good:** Wave 1 builds models (testable in isolation). Wave 2 builds service (tested against real models). Wave 3 builds handler + router (tested with real service). Each wave proves something before the next depends on it.

## Parallelism Budget

More parallel agents = faster wall-clock time but less verification per brick. You become a merge bot instead of an engineer.

Cap at 3 parallel agents per wave — because verification is the bottleneck, not production. If more bricks are ready, split into sub-waves. This forces you to actually engage with each agent's output before the next batch buries it. A previous sprint ran 5 agents in parallel — the orchestrator could not meaningfully review 15 new files between waves and missed fundamental bugs in all of them.

The constraint isn't the tooling. It's your attention. Agents produce code faster than you can verify it. If verification lags production, bugs compound across waves.

## Wave Readiness Check

Before dispatching wave 1:
- Every brick can be independently tested without other unbuilt bricks
- Every implementation brick has `guarantees_tested` per `brick-design.md` — named test + named assertion
- No acceptance criteria says only "tests pass" — see `brick-design.md` Acceptance Criteria for why
- Verification commands (test + runtime) are defined in context.md
