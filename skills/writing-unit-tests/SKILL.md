---
name: writing-unit-tests
description: Write valuable unit and integration tests (or work test-first with Red-Green TDD) that catch real bugs. Test uncertainty not certainty, confirm public seams first, mock only external boundaries, avoid tautological tests, and require a feature verification test. Use when writing tests, doing TDD, reviewing tests, checking mocks, or verifying a feature works. Triggers on 'test', 'unit test', 'tdd', 'red-green', 'mock', 'coverage', 'verify feature'.
---

# Writing Unit Tests

Test where bugs hide, not where code is obvious. Read `GLOSSARY.md` (if present) so test names read like specs in the project's domain language, and respect `docs/adr/` in the area you're touching.

## Core rule

**Test uncertainty, not certainty. Every test must be able to fail.**

If deleting your implementation doesn't break the test, delete the test.

## Confirm seams before writing tests

Tests live at **public seams** (the interface callers use), never against private internals. Before writing tests for a feature, list the proposed seam(s) with a one-line note on what each catches and what it misses, and confirm with the user so testing effort lands on critical paths instead of low-value helpers.

## The 6 laws

1. **Behavior not implementation** — assert outputs/side effects users see, not internal calls or private state.
2. **Your code not frameworks** — don't test builtins, getters, constructors, library behavior.
3. **Mock at boundaries only** — mock external APIs, DB, clock/random. Don't mock your own code or fast pure functions.
4. **One test, one thing** — complex test = bad code, refactor first.
5. **Delete bad tests** — bad tests are worse than none (false confidence + maintenance).
6. **Never write tautological tests** — don't recompute expected values using the same formula as the code (`expect(add(a, b)).toBe(a + b)`). Expected values must come from an independent source of truth: a known-good literal, worked example, or spec.

## Vertical Red → Green loop (when doing TDD)

When building a feature or fixing a bug test-first, work in **vertical slices — one test at a time**:
1. **Red:** Write one failing test at an agreed seam and run it to confirm it fails for the right reason.
2. **Green:** Write the minimal code to make that one test pass.
3. **Repeat:** Move to the next behavior slice. Never write all tests up front before any implementation exists (horizontal slicing commits to imagined structure). Save cleanup/refactoring for the review stage.

## Should I write this test?

```
Framework mechanics? YES -> delete
User wouldn't notice breakage? YES -> don't write
Another test covers it? YES -> don't write
Else -> write it
```

## Mock ladder (highest confidence first)

1. Real thing — no gap
2. Controlled real — tmpdir, in-memory DB
3. Observable fake — counter/channel tracks calls
4. Fake with logic — in-memory store
5. Stub — canned return, document assumption
6. Mock — configured expectations, last resort

Rule: `mock?` External/expensive/non-deterministic = yes. Your class/pure/config = no.
Red flag: 5+ mocks = design problem, not test problem.

See `references/anti-patterns.md` for bad vs good pairs.

## Feature verification (required for done)

Every feature needs ONE new test proving happy path works:

- Did not exist before your feature
- Exercises new code path
- FAILS if you delete implementation

```
GOOD: test_synonyms_appear_in_prompt() - proves feature
BAD: 24/24 existing tests pass - proves nothing about new code
```

Need both regression (nothing broke) + verification (feature works). Only verification lets you declare done.

## Checklist before done

```
□ Behavior users see?
□ OUR code not framework?
□ One thing per test?
□ Mocks only boundaries?
□ Side effects observable (not silent no-op fake)?
□ Fails if implementation deleted?
□ Name: test_<behavior>_<condition>_<expected>?
```

## Notes

- For helper scripts, run `script --help` first instead of reading the source into context.
- Tool names per host (Claude Code, opencode, Antigravity): `../_shared/hosts.md`.
