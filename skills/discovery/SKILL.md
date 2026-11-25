---
name: discovery
description: Turns a fuzzy idea into clear, numbered requirements or a reasoned decision before any design work, while maintaining the project's GLOSSARY.md and ADRs (docs/adr/). Two modes - Grill (the user knows what they want but details are missing) and Brainstorm (the direction itself is unclear). Use when an idea is vague, before writing a spec or design, when exploring "should we / what if", or when aligning on project terminology.
---

# Discovery

Understand the problem before solving it. Building on a misread requirement is
the most expensive mistake in a project, because everything downstream inherits
it. This skill has two entry points; pick by what's unclear:

- **Grill** when the user knows the goal but the details are missing
  ("add notes to my study tracker", "this page doesn't feel complete").
- **Brainstorm** when the direction itself is open ("should we cache or queue?").

In both modes, **finding facts is your job, never the user's.** When you need
a fact from the codebase, dispatch a fresh-context explorer subagent on the
fast tier (see `../_shared/hosts.md`) instead of loading dozens of files into
the main chat. That keeps the main session in the Smart Zone and respects the
user's attention.

## Grill: extract requirements in Frontier Rounds

The core rule: **never invent a requirement.** Every requirement must trace
back to the user's words or existing code; anything else is an open question.

Map the interview as a **design tree** — each decision branches into the
decisions that hang off it — and work the tree in **rounds**:

1. **Read shared language first:** Check `GLOSSARY.md` (or `GLOSSARY-MAP.md`),
   `docs/adr/`, `CLAUDE.md`/`AGENTS.md`, and relevant specs. Dispatch a
   fast-tier explorer subagent to scout the affected code area.
2. **Ask the whole frontier in one round:** The **frontier** is every decision
   whose prerequisites are already settled (independent questions you can ask
   *now* without guessing answers you haven't heard). Don't block on a running
   explorer subagent — only questions downstream of its lookup wait; ask the
   rest of the frontier immediately. Format each round like this:

   ```markdown
   ❓ **Q1** - **<short title>**: <question, with clear choices if helpful>

   ➡️ <your recommended answer>

   ---

   ❓ **Q2** - **<short title>**: <question>

   ➡️ <your recommended answer>
   ```

   Word each question so replying **"yes"** accepts your recommended answer.
   Hold back any question that depends on an unanswered question in the current
   round — it belongs to a *later* round.
3. **Cover the branches people forget:** Use `references/question-bank.md`
   (users/auth, empty/loading/error states, exact validation wording, mobile vs
   desktop, double-submit, refresh mid-flow, timeouts) so real edge cases surface
   before coding.
4. **Sharpen domain language & docs inline:** Follow
   `references/domain-modeling.md` during the conversation:
   - Call out conflicts with `GLOSSARY.md` or existing code immediately.
   - Update `GLOSSARY.md` inline (lazily created) with canonical terms and
     `_Avoid_` synonyms — no implementation details.
   - Offer a short ADR in `docs/adr/NNNN-slug.md` only when a decision passes
     all three ADR filters (hard to reverse, surprising without context, real
     trade-off).
5. **Stop when the frontier is empty:** Every branch visited, nothing silently
   assumed, or the user says to build. Confirm shared understanding before
   acting.

Write the settled requirements to `tasks/YYYY-MM-DD-<slug>.requirements.md`:

```markdown
# <Topic> — Requirements
Source: discovery session, <date> / Status: COMPLETE | PARTIAL

## <Area>
- R1: requirement in plain language
- R2.1: sub-requirement

## Open Questions
- [OPEN] what's unresolved, and why

## Next Step
→ software-design | implementation-plan
```

Write requirements in plain language using the project's `GLOSSARY.md` terms,
not implementation details. Number them (`R1`, `R2.1`) so designs, plans, and
tests can cite them.

## Brainstorm: choose a direction

First, stabilize the question:
- **Decision:** what exactly is being decided
- **Job:** the outcome it serves
- **Constraints:** facts that bound the answer
- **Unknowns:** what, if learned, would change the winner
- **Success:** what "good enough" looks like
- **Cost of error:** how bad a wrong choice is, and how reversible

Tag evidence as `KNOWN` (observed), `INFERRED` (follows from known facts),
`ASSUMED` (provisional), or `UNKNOWN`, so solid facts stay separate from guesses.

Treat your first answer as a candidate, not a conclusion, and try to disprove
it: What must be true for it to win? What's the strongest alternative, and what
observation would distinguish the two? What weakens the favorite?

Match rigor to stakes:
- **Two-way doors** (cheap to reverse, quick feedback): decide and learn.
- **One-way doors** (migrations, public APIs, databases, destructive or slow
  changes): require real alternatives and a failure analysis before deciding.
- Keep the scope fixed; don't quietly broaden the question.

A brainstorm lands in one of three places: a decision with the condition that
would reverse it, "don't build", or "spike first" (the smallest experiment that
makes the difference observable). Record it with
`references/commitment-template.md`, and if it passes the 3-part ADR filter in
`references/domain-modeling.md`, save a concise ADR in `docs/adr/NNNN-slug.md`.

## Notes

- Ask only questions whose answer changes what you'd build.
- Tool names and subagent spawning per host: `../_shared/hosts.md`.
