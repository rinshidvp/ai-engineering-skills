# Creating a Design

Full workflow from spec to design doc. Read this when starting a new design.

## Read First

Before proposing anything new:
1. Read active task or sprint design docs if they exist
2. Read module-level `DESIGN.md` files near the affected code
3. Read the CONTRACT blocks of dependencies you expect to use
4. Note reusable infrastructure, existing abstractions, established patterns

Reuse existing good boundaries. Do not redesign from zero unless current structure is the problem.

## 1. Normalize the Problem

Turn raw spec into a problem model before designing the solution.

**Technique:** Read spec, highlight nouns and verbs = essential complexity (business problem). Cross out databases, frameworks, tools = accidental complexity (implementation choices). Build nouns and verbs first.

Extract:
- user-visible outcomes
- actors and callers
- primary entities and state
- workflows and business rules
- invariants that must always hold
- external systems and integrations
- non-functional constraints
- unknowns and ambiguities

Separate requirements from implementation hints.
Bad: "Use Postgres and Redis" as architecture.
Good: "Needs durable storage and low-latency lookup" as requirement; technologies negotiable.

## 2. Run the Discovery Engine

If you cannot answer the questions below, you don't understand the problem well enough. Stop and get clarity.

Produce a discovery memo using these lenses. Each reveals different boundaries:

**Volatility map** — where change hits, so boundaries contain it.
- What is most likely to change in 12 months?
- Which boundaries would contain those changes?

**Core vs shell** — pure decision logic vs side-effects (I/O, persistence, transport, scheduling). Pure logic = easy to test, no mocks. Side-effects belong in shell core doesn't know.
- What is pure decision logic?
- What is only I/O, persistence, transport, scheduling, integration?

**Failure domains** — isolate so one failure doesn't cascade.
- If each dependency goes offline, what must gracefully degrade?
- What is allowed to fail?
- How is blast radius contained?

**Data lifecycle** — trace primary entity through transformation phases.
- Trace entity/state transition through feature
- Identify distinct phases of transformation

**State ownership** — who owns mutation, prevents distributed state bugs.
- Who owns mutation?
- What is persisted vs derived?
- Where do idempotency, caching, ordering, concurrency control live?

## 3. Build the Layer Stack

Start with layers before components. Layering is a main decomposition tool, not cleanup.

Each layer absorbs one kind of mess so layer above stops thinking about it. Justified only when it actually collapses complexity. If it just forwards calls and renames methods = ceremony, delete or merge.

For each layer, state:
- what complexity it hides
- what API or model it exports upward
- what lower layers it depends on
- what it explicitly does not know about

Typical shape:
```
Infrastructure / Adapters   -> raw I/O, transport, persistence, retries, serialization
Service / Adapter Layer     -> stable abstractions over external systems
Domain Layer                -> entities, invariants, domain operations
Application / Use Cases     -> workflows, orchestration, policy decisions
```

Bad: domain logic catches HTTP 429, parses JSON.
Good: lower layer maps transport behavior into domain-level error before crossing boundary.

## 4. Generate and Evaluate Candidate Decompositions

Don't stop at first reasonable cut. Check if known pattern solves this shape (hexagonal, pipeline, event-driven, CQRS, repository+service, strategy, etc.). If fits, use as candidate and name pattern.

Generate at least 2 candidates for moderate, 3 for major. One must be layer-first. Others use different lenses:
- data lifecycle or pipeline stages
- bounded contexts or domain concepts
- trust or privilege boundaries
- failure isolation

For each candidate, state:
- components — each with single, clearly stated responsibility
- ownership — what data and behavior each owns exclusively
- boundaries — interfaces between components
- main dependency direction
- known pattern it draws from (if any)
- key trade-off

Apply SRP at every level: component, module, package, method = one reason to change. Can't state responsibility in one sentence = doing too much.

Design components as focused, composable units with explicit interfaces. Dependencies point inward toward domain logic. Components interact through interfaces, not concrete implementations = swappable, independently testable.

## Compare candidates on two axes:

*Engineering quality* — isolates change, hides complexity, protects boundaries (encapsulation, abstraction quality, extensibility).

*Simplicity* — simplest design solving actual problem, not building for hypothetical futures (KISS, YAGNI).

These pull against each other. Name tension explicitly:
- Strong boundaries but over-engineered? Ask: solving real problem within 12 months or hypothetical?
- Simple but weak boundaries? Ask: will simplicity survive first requirement change or shatter?

Right design = simplest whose boundaries hold when likely changes actually change.

**Recommend one candidate.** State:
- which and why
- what it trades off
- why rejected lose — specific scenario/force making them wrong cut
- what would change your mind — assumption that, if wrong, means wrong design

## 5. Define Component Contracts

Only after decomposition chosen. Design identifies what contract *should* be. Actual CONTRACT blocks in code written during implementation with concrete context.

For every component, specify:
- **GUARANTEES** — specific, testable
- **EXPECTS** — preconditions
- **FAILURE BEHAVIOR** — deterministic per failure mode
- **DOES NOT** — explicit refusals
- **KNOWN LIMITATIONS** — deliberately not handled
- **EMITS** — logs, metrics, events (when operationally important)

Keep system-wide blast-radius in design doc, not every component contract.

## 6. Surface Assumptions

List assumptions design depends on. For each:
- the assumption
- what invalidates it
- fallback if wrong

Assumptions not written down survive only in current conversation. Not good enough.

## 7. Pressure-Test the Design

Walk design through failure and change before treating as complete.

**Scenario checks:**
- **happy path**: contracts compose cleanly end to end
- **outage test**: dependency offline — failure contained?
- **change test**: requirement changes or "swap provider" — how many components change? >1 = boundary leaked
- **testability test**: core logic testable with plain data, no mocks, no network?
- **deletion test**: feature removable without surgery across unrelated code?

**Per-component checks:**
- **Blast radius**: contract change → how many files update? Acceptable = as few as possible, ideally one.
- **Local reasoning**: open component source, understand without reading rest of system? If no = knows too much.

If scenario forces component into another's internals, boundary is wrong.

## 8. Document the Design

Design artifact = blueprint future agent builds from with no additional context. You're *proposing* design, not implementing.

**Where design doc goes:**
- If spec exists (e.g. `tasks/user-notifications.spec.md`), name to match: `tasks/user-notifications.design.md`
- If no spec: `tasks/YYYY-MM-DD-<topic>.design.md`

Stays in `tasks/` as proposed artifact. During implementation, promoting agent moves it to `<module>/DESIGN.md` alongside code. See `references/implementing.md` for promotion process.

**What it contains:**
- problem model
- reusable existing pieces
- discovery memo
- layer stack
- candidate decompositions with trade-offs
- chosen decomposition and rationale
- component contracts (intended guarantees, expects, failure behavior, does not)
- assumptions and fallbacks
- validation scenarios
- open questions and out-of-scope items