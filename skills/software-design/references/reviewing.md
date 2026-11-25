# Reviewing a Design

Read this when checking a design for soundness, or code against design.

## Pre-implementation: Is the design sound?

Hand the design to a separate agent with no other context. Prompt:

> "It's 6 months from now and this system failed in production. Review the design — find the holes in correctness, robustness, and fault tolerance."

Do not bias the reviewer with specific concerns — let it find problems independently.

## Post-implementation: Is the code faithful to the design?

Check three things:

**1. DESIGN.md exists and is current.** Every module with 2+ components has a DESIGN.md. It describes decomposition rationale and component relationships. It matches the actual code — no references to renamed/deleted components, no missing new ones.

**2. CONTRACT blocks exist and are consistent.** Every component's main source file has a CONTRACT block with GUARANTEES, EXPECTS, FAILURE BEHAVIOR, DOES NOT. Contracts consistent with what DESIGN.md describes.

**3. Contracts are tested.** Every GUARANTEE has a test proving it holds. Every EXPECTS violation has a test proving it's rejected. Every FAILURE BEHAVIOR has a test triggering that failure.

Prompt for a documentation review agent:
> Read DESIGN.md in <modules>. Read CONTRACT blocks in every source file.
> Check: (1) Does DESIGN.md describe every component that exists in code?
> (2) Does every source file have a CONTRACT block? (3) Are the CONTRACT blocks consistent with DESIGN.md? (4) Is every GUARANTEE tested?
> Report gaps, inconsistencies, and untested guarantees.

## Design quality signals

**Healthy design:**
- Small, focused files — each under 300-400 lines
- Each component has one clearly statable responsibility
- Interfaces between components, not concrete coupling
- Domain logic is pure — free of I/O, HTTP, SQL, file system
- Core logic testable with plain data, no mocks
- A likely requirement change stays within one component
- A component can be deleted without surgery elsewhere

**Sick design** (see `references/design-smells.md` for full catalog):
- **Implementation leaking** — callers import types named after implementations
- **God classes** — one class doing everything, 10+ methods spanning unrelated concerns
- **Large files** — over 700 lines = multiple responsibilities tangled
- **Shotgun surgery** — one business rule change touches 5+ files
- **Infrastructure in domain** — domain code importing DB drivers, HTTP clients
- **Mock-heavy tests** — 10 mocks to test a business rule = design problem

## Periodic checks

- **Contract compliance:** Does implementation still honor every GUARANTEE?
- **Boundary integrity:** Are components accessing each other's internals?
- **Assumptions:** Are listed assumptions still valid?