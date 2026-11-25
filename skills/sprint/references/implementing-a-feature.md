# Implementing a Feature

For small-to-medium features. For larger work needing parallel agents and wave gates, use the `sprint` skill.

---

You're a tech lead with a team of engineers. Coders build from your designs. Clerks handle exploration, test runs, and mechanical work. What ships is under your name.

Your job: study the codebase, design the plan, write clear briefs, maintain shared context, review every change, certify quality. You don't type code unless it's genuinely faster than briefing someone. Your context window is finite — every file you read for a mechanical edit is context you can't use for the work only you can do: decisions, review, synthesis. When context runs out, the lead is gone.

Agents are capable but unsupervised work drifts. They hardcode what should be configurable, duplicate what should be shared, skip edge cases that aren't in the brief. This is production code. You review actual files after every wave, flag issues specifically, and send the same agent back to fix its own work.

```
               YOU (tech lead)              CODER              CLERK
               ───────────                  ─────              ─────
  ┌─────────┐
  │ 1 STUDY │── synthesize ◄─────────────────────────── explore codebase
  └────┬────┘                                            (parallel)
       │
  ┌────▼────┐
  │2 DESIGN │── you own this
  └────┬────┘   (use software-design skill)
       │
  ┌────▼─────┐
  │3 VALIDATE│── pause for user approval
  └────┬─────┘
       │
  ┌────▼───┐
  │4 SPIKE │── you judge ◄─────── run scripts ──────── run scripts
  └────┬───┘
       │
  ┌────▼──────────┐
  │5 CLASSIFY     │  implementation ──► coder
  │               │  mechanical ──────► clerk
  └────┬──────────┘  independent? ────► parallel
       │
  ┌────▼──────────┐   ┌───────────────────────┐  ┌──────────────┐
  │6 EXECUTE      │   │ Wave A (parallel):    │  │ clerk runs   │
  │  + CERTIFY    │◄──│  coder ► piece 1      │  │ make check   │
  │               │   │  coder ► piece 2      │  │ + tests      │
  │  review files │   ├───────────────────────┤  │ each wave    │
  │  log evidence │   │ Wave B (needs A):     │  └──────────────┘
  │  to progress  │   │  coder ► piece 3      │
└────┬──────────┘   └───────────────────────┘
        │
   ┌────▼──────────┐
   │7 QA + REVIEW  │── adversarial tester: tests from spec only (no code access)
   │               │── impl-reviewer: spec vs diff (completeness)
   │               │── code-reviewer: diff (correctness, maintainability)
   └────┬──────────┘
        │
   ┌────▼──────────┐
   │8 FINAL VERIFY │── run the real thing, show actual behavior
   └───────────────┘
```

> Role map: `clerk` = runner (fast tier), `coder` = builder (strong tier). The Agent Selection table in `orchestration-pattern.md` is the source of truth; tier → model per host is in `../../_shared/hosts.md`. Legacy names in this file map accordingly.

## Documents

Every task: `tasks/<YYYY-MM-DD>-<slug>/`

| File | Purpose |
|---|---|
| `context.md` | Cumulative: codebase findings, decisions, learnings, gotchas. **Pass to every agent brief.** Update after each wave. |
| `design.md` | Component breakdown, contracts, decisions |
| `progress.md` | Wave certifications with evidence, issues found, resolutions |

## 1. Study

Send explore agents to scan the codebase in parallel. You synthesize their findings — don't read every file yourself. Write findings to `context.md`.

- What patterns, types, abstractions exist that you can build on?
- Where does this feature naturally fit?
- What would you be reinventing?

## 2. Design

Use the `software-design` skill for non-trivial decomposition. Write the result to `design.md`.

For simpler work, decompose into components with clear contracts (GUARANTEES / EXPECTS) yourself.

## 3. Validate

Share `design.md` with the user. Wait for explicit approval. Do not implement without it.

## 4. Spike

If any assumption is unvalidated — library behavior, API shape, data format — have an agent spike it. Add findings to `context.md`.

## 5. Classify pieces

Before touching files, classify every piece:

| Work type | Who |
|---|---|
| Implementation from solid design | **coder** |
| Mechanical / bounded (grep, fixtures, known patterns) | **clerk** |
| Exploration / research | **clerk** (explore) |
| Design, review, certification | **you** |

**Default is delegate.** The design is the brief. Self-build only when briefing costs more than the edit.

Group independent pieces into waves. Waves run sequentially; pieces within a wave run in parallel.

## 6. Execute and certify

**Plan your agents before spawning.** Map pieces to named agents. Name them by role or wave (e.g., `email-coder`, `dash-coder`). When an agent needs to fix its own work, use `SendMessage` to send it back — it already has full context of what it built and what went wrong. Spawning a fresh agent for rework wastes tokens on re-reading.

For each wave:

1. **Brief agents** — files, orient list, pattern, done-criteria, path to `context.md`. Independent agents in a single message.
2. **Review actual files** when complete. Look for: hardcoded values, duplicated logic, wrong patterns, missed callers, magic strings.
3. **Send the same agent back** with specific issues if sloppy. Don't spawn a new one — the original has context.
4. **Clerk runs** `make check` + tests.
5. **Certify in `progress.md`** — status, evidence (test counts, files reviewed with findings), issues found and fixed, context.md updates.
6. **Update `context.md`** with learnings for the next wave.

Next wave only after current is certified.

## 7. QA and review

After all waves certified:

| Gate | Agent role | Input | Catches |
|---|---|---|---|
| Feature tests | adversarial tester (strong model) | Spec only — no code access | Tests that prove new behavior works (not just old tests pass) |
| Completeness | completeness review (strong model) | Spec/design + diff | Missed callers, unhandled edge cases, spec gaps |
| Correctness | `code-reviewer` (strong model) | Diff | Architecture, bugs, maintainability |

A runner subagent (cheap/fast model) runs the adversarial tests. Failures are bug reports — fix the implementation, not the tests. Log findings in `progress.md`.

**When to use which gates:**

| Condition | Gates |
|---|---|
| Spec with observable guarantees | All three |
| >3 files changed, no formal spec | completeness review + code-reviewer |
| Small, isolated change | code-reviewer only |

## 8. Final verification

Run the real thing. Show actual behavior — curl response, screenshot, rendered email, generated PDF. Not test output. Log in `progress.md`.

---

## Skills and agents

| Skill / Agent | When | Phase |
|---|---|---|
| `software-design` (in-repo) | Non-trivial decomposition | 2 |
| _spec_ (optional — inline process in sprint `references/planning-funnel.md`) | No spec exists, feature needs observable guarantees | Before 1 |
| testing discipline (`references/agent-guidelines.md`) | Before writing any tests | 6, 7 |
| adversarial tester (strong model) | Spec exists, need adversarial feature tests | 7 |
| completeness review (strong model) | After all waves, check completeness | 7 |
| `code-reviewer` (in-repo `agents/`) | After all waves, check correctness | 7 |
| builder (strong model) | Implementation | 6 |
| runner / explorer (cheap/fast model) | Exploration, test runs, mechanical work | 1, 4, 6 |

No spec → adversarial tester and completeness review have nothing to test against. For non-trivial features, write the spec first (see sprint `references/planning-funnel.md`).

---

## Writing agent briefs

Every brief costs tokens — yours and the agent's. Make them count.

**Structure:**
```
Read tasks/<date>-<slug>/context.md first.

[What] Add role field to the notification service — same pattern as existing status field.
[Files] src/services/notification.ts, src/types/events.ts, src/handlers/webhook.ts
[Pattern] See how status is threaded through EventContext → handler → renderer.
         Same approach: add role to the type, thread through callers, render with ROLE_LABELS.
[Done] make check passes. Notifications include role label for both admin and member events.
[Watch] Use ROLE_LABELS lookup — don't hardcode display strings.
```

**Principles:**

- **Orient with an annotated file list.** Agent starts cold. List each relevant file with a 10-20 word note on what it is and why it matters to this task. Like a tech lead pointing at the codebase on day 1.
- **Give paths, not contents.** Agent reads files itself. Dumping content into the brief wastes your tokens.
- **Name the pattern, don't explain it.** "Thread like status" > "add the field to the interface, then update every caller to pass it through." The agent knows what threading means.
- **Prime the quality bar.** "This is production — maintainable, typed, no shortcuts" activates more care than listing 10 rules.
- **State done-criteria concretely.** "make check passes + role label renders" is verifiable. "Implementation complete" is not.
- **One `[Watch]` line** for the specific mistake this agent will make on this task. Not a general checklist.
- **Reference prior waves.** "Wave 1 added role to event types — see context.md for the pattern" lets the agent build on prior work instead of re-discovering.

**Bad brief** (tutoring, dumping context, vague done):
```
I need you to update the notification service. The notification service
is in src/services/notification.ts. It currently sends notifications
without including the user's role. We need to add the role field. The
roles are "admin", "member", and "viewer" and their display labels are
in ROLE_LABELS in constants.ts. You'll need to update the EventContext
type first, then update the handler, then update the renderer to
actually display the label. Please make sure everything compiles...
```

**Good brief** (compound terms, pattern reference, file orientation, concrete done):
```
Read tasks/<date>-<slug>/context.md first.

Thread role through the notification pipeline — same pattern as status.
Use ROLE_LABELS for display.

Orient:
- src/types/events.ts — EventContext type, add role here (see status field for pattern)
- src/services/notification.ts — builds context and calls handlers, thread role through
- src/handlers/webhook.ts — renders the notification, use ROLE_LABELS[role] for display
- src/constants.ts — ROLE_LABELS lives here, already exported

Done: make check passes. Admin and member events render their role label.
```

---

If you find yourself working around tangled code, stop and flag it. Recommend cleanup before continuing.
