---
name: debugging
description: Systematic bug investigation that moves from competing hypotheses to runtime evidence to a confirmed root cause before any fix. Use when behavior is surprising, the cause is unknown, a bug is flaky or intermittent, or an explanation so far is an unverified guess ("why is this happening", "it sometimes fails", "root cause").
---

# Debugging

Reading code tells you what *should* happen. Only running it tells you what
*does* happen. Most wasted debugging time comes from fixing the first plausible
explanation without checking it, which often patches a symptom and leaves the
real cause in place. This skill makes you prove the cause before you change
anything.

Read `GLOSSARY.md` and relevant `docs/adr/` first if present. **Redact every
secret** (`<REDACTED>`) before showing commands, logs, or captured outputs.

## Phase 0: Build & minimise a tight red-capable repro loop

Before guessing causes, build **one fast, repeatable command** (failing test,
curl/HTTP call, CLI command, or headless browser script) that triggers the
user's exact symptom and **goes red** in seconds.

- **Shrink it:** Cut inputs, steps, and data one at a time until every
  remaining piece is load-bearing (removing any piece makes it go green).
- **If you cannot reproduce it:** Stop, list what you tried, and ask the user
  for a redacted log/trace or environment access. Do not hypothesise blind.

## Phase 1: Form competing hypotheses

Write down at least two plausible explanations. If you can only think of one,
that's a sign you've already anchored on it, so look harder for an alternative.

For each hypothesis, note:
- **H1**: the explanation, in one sentence
  - Confirmed if: what you would observe if it's true
  - Refuted if: what you would observe if it's false
  - How to observe: the log, request, inspection or test that tells them apart

Share the list with the user before investigating. They often know which
explanation is already ruled out, and it keeps you from quietly picking a winner.

## Phase 2: Observe at the boundary

Look at the point where you believe things go wrong, at runtime. If the data
looks wrong, log the data. If the rendering looks wrong, inspect the DOM. If an
API call looks wrong, read the raw response rather than the code that parses it.

Add the minimum instrumentation needed, reproduce the bug, and collect the
evidence. **Tag every temporary debug log** with a unique prefix like
`[DEBUG-a4f2]` so cleanup is a single search-and-delete. Save the exact command
or steps that reproduced it; you'll reuse them to verify the fix.
`references/observation-methods.md` lists methods by situation.

## Phase 3: Confirm or refute

Compare what you observed with each hypothesis's predictions:
- **Confirmed**: the observation matches the prediction. Move to the fix.
- **Refuted**: the observation contradicts it. Cross it off.
- **Inconclusive**: the observation can't tell them apart. Design a sharper one.

If every hypothesis is refuted, return to Phase 1 with what you've learned.
When you report a result, show the evidence (the log line, the response body,
the screenshot), not just "H2 confirmed", so the user can check your reasoning.

## Phase 4: Fix, only after confirmation

Before writing code, answer:
1. Does this fix the root cause, or just the symptom?
2. Does the fix belong here, or upstream where the bad state originates?
3. Are there at least two ways to fix it, and what does each trade off?
4. What else depends on the code you're changing?

Present the approach, then implement it:
1. Turn the minimised repro into a **failing regression test** at the right
   public seam (if no clean seam exists, flag that architectural gap).
2. Apply the fix and watch the regression test + original Phase 0 loop go green.
3. **Cleanup:** search and delete every `[DEBUG-...]` log and throwaway file,
   and state the confirmed root cause in the commit/PR message so the next
   debugger learns.

## Defaults that keep bugs visible

- Fail fast. Avoid `except: pass`, silent fallbacks like `x or default`, and
  catch-all handlers unless you've established why the failure is safe to ignore.
  They hide the next bug.
- Uncertainty in the code is a reason to investigate, not to add defensive code
  around it.
- Tool names for reading, searching and running commands on your host:
  `../_shared/hosts.md`.
