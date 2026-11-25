# Brick Design

A brick is a building block, not a task. The difference matters.

When you build a brick, another agent — one who has never seen your code, never read your reasoning, never talked to you — will depend on it. They'll import your types, call your functions, build their entire brick on the assumption that yours works. They're trusting you. Not because they checked — because the system told them your brick passed.

That trust is the entire architecture. When brick 003 declares `depends_on: ["001"]`, it's not a scheduling hint. It's a contract: "I believe 001's guarantees. I will build on them." If you shipped 001 with a shoddy check — it compiles, the imports resolve, close enough — then 003 builds on a lie. And 004 builds on 003. And by the time someone discovers that `deriveEventCost` silently returns the wrong number, there are 13 bricks downstream and all of them are contaminated.

That's not a hypothetical. A real sprint shipped 14 bricks. Every single one "passed" — `tsc --noEmit` exited clean, agents reported success. The app made infinite API calls on load. Two pages crashed. Layouts were broken. Every bug traced back to foundation bricks that compiled but were never actually verified. The entire sprint's output was trashed.

**When you build a solid brick — one that genuinely works, not one that merely compiles — every brick built on top of it succeeds partly because of you.** Your `formatCurrency` that handles null correctly means the Sessions page displays "—" instead of crashing. Your `classifyBubbleState` that was tested with real inputs means the Overview page shows the right animation. Your work carries theirs.

When you fake it — when you check that it compiles and call it done — you're not saving time. You're spending someone else's time. The agent building on your brick will debug a problem that isn't in their code. The orchestrator will waste a wave tracking down why the integration broke. The user will open the app and see it's broken and the whole sprint gets questioned.

**Every brick must prove it holds weight before the next wave builds on it.** How it proves that depends on what it is:

- A pure function brick proves it with tests — call the function, assert the output
- A UI component brick proves it by rendering — start the app, load the page, the component appears correctly
- A CLI command brick proves it by invocation — run the binary with specific arguments, assert exit code + stdout + file system state
- An integration brick proves it by running the system — the pieces connect, data flows through
- A wiring brick proves it by the software loading with the new routes, the new config, the new provider

The form of evidence varies. The requirement doesn't: **something must be observed that would fail if the brick were wrong.** "It compiles" is necessary but not sufficient — compilation proves internal consistency, not correct behavior. The question isn't "does my code have errors?" It's "would the next agent be right to trust this?"

## Schema

Add bricks by editing `tasks/<task-name>.tasks.json` directly — append to the `bricks` array.

```json
{
  "id": "001",
  "name": "Short descriptive name",
  "description": "What to build. Reference files, patterns, existing code.",
  "acceptance_criteria": "1. Specific condition. 2. Named test + named assertion.",
  "status": "pending",
  "depends_on": ["other-brick-ids"],
  "type": "implementation|discovery|integration|test",
  "tags": ["area", "component"],
  "files": ["paths/this/brick/will/create-or-modify"],
  "guarantees_tested": ["GUARANTEE_NAME: specific test name + assertion"]
}
```

`guarantees_tested` — required for `type: "implementation"`. Name the guarantee, name the evidence. If you can't fill it in, the design is missing or the brick is too high in the tree. For unit-testable bricks (pure functions, data models), this means a test file and a named assertion. For bricks that can't be unit-tested (UI components, integration wiring), this means a runtime verification step — what do you observe to confirm it works?

Ask at design time: "How will the wave gate verify this brick?" If the answer is "it compiles" — the brick's guarantees are unverified and everything downstream is at risk.

## Sizing

Each brick = one agent session. Can a coder agent complete this with a clear prompt and no scope ambiguity?

**Too broad:** "Set up the data layer" — unclear when done.
**Right-sized:** "Create User and Session models in models.rs with serde derives and default impls" — one agent, clear files, testable output.

## Acceptance Criteria

Write criteria that a failing feature would fail.

**Bad:** "Models work correctly." / "Tests pass."
**Good:** "1. User struct has id, name, email fields with serde derives. 2. `cargo test models::tests::test_user_default` → asserts `user.name == ""`."

Structural vs behavioral:
- Structural: `cargo test passes` — proves it compiled
- Behavioral: named test + named assertion — proves the guarantee

Pre-mortem test: "This shipped and broke. What specific test catches it?" If you can't name it, rewrite the criteria. For bricks that can't be unit-tested, the pre-mortem answer depends on the domain — "start the app and the page crashes" (web), "run the binary and it panics on valid input" (CLI), "start the server and the endpoint returns 500" (API). That's valid evidence, as long as the wave gate actually exercises the software.

**CONTRACT blocks:** If the brick creates a new source file, include in acceptance criteria: "CONTRACT block at top of `<file>` documenting GUARANTEES, EXPECTS, FAILURE BEHAVIOR, DOES NOT." The agent writing the code writes the contract — it has full context. A separate agent writing the contract later produces weaker guarantees.

## The `files` Field

Every brick MUST list files it will create or modify. The parallel execution engine uses this.

**Bad:** omitting files, listing "various files."
**Good:** `["server/src/models.rs", "server/src/models.test.rs"]`

For unit-testable bricks, include both source and test files. For bricks verified at runtime, list the source files and note the verification method in acceptance criteria.

If two bricks share a file: merge them, restructure to touch different files, or add a dependency so they run sequentially.

## Design Contracts

Brick dependencies come from contracts, not intuition. Before decomposition for any multi-component or multi-layer feature, a **validated** `design.md` MUST exist — with components, layers, and GUARANTEES / EXPECTS / FAILURE BEHAVIOR per component.

The design must be validated by the user before bricks are decomposed. Component layers, abstractions, and contracts are load-bearing; getting them wrong upfront cascades into every brick downstream.

Brick boundaries are derived from the design's contracts. A brick that can't reference a guarantee from the design is either too high in the tree or working from a missing design — in either case, fix the design before continuing.
