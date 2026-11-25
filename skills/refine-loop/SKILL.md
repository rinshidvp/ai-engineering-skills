---
name: refine-loop
description: A capped polish loop for any artifact (code, spec, design, plan) - build, get an independent review through a skill lens, fix what's real, verify, at most two passes. Use when work needs an independent review-and-fix cycle ("refine this", "review loop", "iterate on this", "polish").
---

# Refine Loop

Produce, get an independent review, fix what's real, verify. **Cap it at two
passes**, and go to a third only if the user explicitly asks.

The cap is deliberate. The first two passes catch real correctness and
structural problems. After that, reviews mostly find issues with the previous
fixes, and the loop turns into polishing on the user's time. A human saying
"good enough" beats a fifth pass.

## Roles

- **Implementer:** builds and fixes from the brief and holds the task context.
  It needs competence in the medium; the judgment comes from the brief.
- **Reviewer:** gives an independent opinion through a skill lens. It is never
  the same agent as the implementer, because an author reviewing their own work
  shares its blind spots. Use the reviewer tier, and make sure it's allowed to
  say "clean".
- **You (orchestrator):** triage both outputs. Don't delegate triage; it's where
  the judgment lives.

Default routing: the strong or fast tier builds (fast only when the brief leaves
nothing to decide), the reviewer tier reviews, and the main session
orchestrates. What those tiers are on your host, and how to spawn them:
`../_shared/hosts.md`. On Claude Code, the `code-reviewer` agent is the
reviewer for code.

## Starting

**Embedded** (a sprint or plan already gave you a contract): the contract is the
plan. Go straight to Pass 1 and report into `progress.md` plus a verdict in chat.

**Standalone** (the user asked for it directly):
1. Work out the artifact and the lens from context (table below).
2. If the depth is unclear, ask once: "Real bugs only, or structural issues
   too?" Default to stopping short of pedantic.
3. Show the plan, `Build (who/using) → Review (who/lens) → Fix (verify how)`,
   with the depth and the two-pass budget, and wait for confirmation.

## Each pass

1. **Pass 1:** brief the reviewer once at the start with scope, lens, goal,
   users, scale and criticality, using `references/reviewer-brief-template.md`.
   Don't add your suspicions; they bias the review.
2. **Triage** each finding as fix now, skip (below the agreed depth), or real
   but out of scope (log it as deferred). If a finding is contested, keep both
   views in the report instead of silently dropping one.
3. **Fix and verify:** the implementer applies only the triaged fixes, then
   runs typecheck, lint and tests.
4. **Report:** conformance (yes / no / partial, taken from the reviewer's
   verdict rather than inferred), passes used, findings found and fixed,
   deferred items, skipped items, and residual risks.
5. **Pass 2:** the same reviewer checks that the fixes landed and does a fresh
   scan of the changed areas. Earlier findings that were settled stay settled
   unless a fix broke the goal.
6. **Stop rules** (never continue past two passes automatically):
   - Pass 1 clean → done.
   - Pass 1 has findings → fix → Pass 2.
   - Pass 2 clean → done; tear down and hand deferred items up.
   - Pass 2 still has findings → stop and ask: "keep fixing, or ship as is?"
   - A severe contested finding, or a reviewer working from the wrong profile →
     stop immediately and escalate.

Agents live for the task, not the pass: keep the same reviewer across both
passes so it remembers what it already flagged, then tear it down. The exception
is critical standalone work with no later milestone review: use a fresh reviewer
for Pass 2.

## Lens table

| Artifact | Apply skill |
|----------|-------------|
| Code changes | `code-quality`, `software-design` |
| Code that should work | `writing-unit-tests` (run the tests; failures are findings) |
| Bug or flaky behavior | `debugging` |
| Requirements or a decision | `discovery` |
| Design doc | `software-design` (reviewing a design) |
| Plan | `implementation-plan` (self-check) |

Interactive lenses, like a discovery grilling session, run directly with the
user rather than through a subagent.

## Notes

- Give the reviewer file paths, not pasted code. It reads what it needs, which
  is cheaper and keeps its view unfiltered.
- Builder and reviewer can run in parallel when it's safe; the reviewer reads
  the branch or worktree as it stands, even mid-build.
- If the fast tier keeps missing the brief, move building to the strong tier.
  It costs more, but less than repeated fix passes.
