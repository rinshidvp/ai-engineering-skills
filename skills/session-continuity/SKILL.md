---
name: session-continuity
description: Preserve and restore context across session boundaries. Create handoff documents, bootstrap new sessions from them, or flush current context into a clean plan file. Use when ending a session, starting fresh, context is getting long, or handing off to another agent.
---

# Session Continuity

You're a business analyst handing off to a new development crew. They weren't in the room for any of this. Every gap in your brief is an hour they'll waste rediscovering — or worse, a wrong assumption they'll build on. Your job is to make sure they never have to guess.

Context windows are long but retrieval is lossy. A single pass over a 200k-token conversation will miss things — decisions buried in a tangent, a user opinion stated once and never repeated, a dead end that looks like irrelevant chatter. The staged process below forces multiple passes, each with a different lens, so the final output is complete.

## Modes

| Mode | When | Output |
|------|------|--------|
| **Session Handoff** | End of session, ongoing work | `tasks/<task>.handoff.md` (living document) |
| **Task Handoff** | Starting a new chat for a specific task | Printed prompt (user copies to new chat) |
| **Bootstrap** | Starting a session from a handoff | Loaded context + summary |
| **Context Flush** | Context too long, need clean slate | Plan mode file |

---

## Staged Extraction (Session Handoff & Task Handoff)

Both handoff modes use this staged process. Do not skip stages or combine them.

### Stage 1: Exhaustive Extraction

Go through the **entire** conversation. Cast a wide net. Don't filter yet — capture everything that could matter.

Load `references/extraction-categories.md` for the full checklist. Work through each category systematically. Tag confidence (high/medium/low) that each item is still current and not overruled later.

The categories you'll tend to skip (force yourself):
- **Dead ends** — they feel like failures, not knowledge. Record what was tried and WHY it failed.
- **Rationale** — the decision feels obvious in context. It won't be obvious to the next agent. Capture WHY.
- **User opinions as constraints** — "I hate X" said in passing is a constraint. Capture it.
- **Approved-with-tweaks** — if the user said "yes but change Y," capture the TWEAKED version, not the original.

### Stage 2: Gap Analysis

Now step back. Play the skeptical new agent who just received your Stage 1 output. Ask yourself:

- What would I be **forced to guess**?
- Are there implicit format details I inferred but the user never confirmed?
- Did the user change their mind on anything? Is only the **final** decision captured?
- Are all decisions accompanied by WHY? Could I unknowingly reverse one?
- Is scope clear enough I won't build things marked "later"?
- If the user said "don't do X" — did I capture that?
- Did I capture exact wording of error messages, labels, field names — or just paraphrase?
- Are there contradictions? Which statement is authoritative?

Write down every gap.

### Stage 3: Reconciliation

Go back through the conversation to resolve the gaps from Stage 2. For each:
- If resolvable: fill it in, citing the conversation point
- If genuinely unknown: mark it **UNSPECIFIED** — the next agent must ask, not guess
- For overridden decisions: state the **current** decision, note what was previously considered

### Stage 4: Distill

Organize the reconciled extraction into the output format.

- **Session Handoff** → load `references/session-handoff-template.md`
- **Task Handoff** → load `references/task-handoff-template.md`

Cut anything that doesn't help the next agent be productive. Verbose enough to eliminate ambiguity, no filler.
- **Use pointers, don't duplicate:** Reference existing specs, plans, ADRs, commits, or diffs by path/hash instead of copying their contents into the handoff.
- **Include `Suggested Skills`:** List the 1–3 skills the next session should load first (e.g., `writing-unit-tests`, `code-quality`).
- **Redact secrets:** Never write API keys, tokens, passwords, or sensitive PII into handoff documents.

---

## Session Handoff

Full knowledge transfer for ongoing work.

**Output:** `tasks/<task-name>.handoff.md` (use repo-relative paths inside committed handoffs so they stay portable across clones/worktrees; print the absolute handoff path in the chat restore prompt below).

**Living document pattern:** Section 1 (Current State) is updated each session to reflect NOW. Section 2 (Session Log) is append-only — never modify previous entries.

**Process:**
1. If handoff exists: read it first
2. Run [Staged Extraction](#staged-extraction-session-handoff--task-handoff)
3. Update Section 1 with current truth (delete stale info)
4. Append new entry to Section 2

**After writing**, print the bootstrap instruction:

```
To restore this session in a new chat, ask the agent to:
"Bootstrap from <ABSOLUTE_PATH_TO_HANDOFF> using the session-continuity skill"
```

---

## Task Handoff (New Chat Prompt)

Scoped knowledge transfer for a specific task in a new chat.

**Output:** Printed to conversation. No file. User copies to new chat.

**Process:**
1. Run [Staged Extraction](#staged-extraction-session-handoff--task-handoff), scoped to the task — discard what's irrelevant
2. The user's reason/task description becomes the "Task" section — what the new agent should do and WHY we're starting fresh
3. Distill using `references/task-handoff-template.md`

**Key rule:** Decisions are settled, not suggestions. Include rationale so the new agent understands but doesn't re-litigate.

---

## Bootstrap

Load a handoff document and restore context. You have zero prior context — the handoff is your map. Trigger phrase: user asks to "bootstrap from <path>".

**Key principle:** The handoff is a navigation map, not source of truth. Files may have changed since it was written. Read the CURRENT state.

### Step 1: Get Handoff Document

If argument provided: read it directly. If not: ask for the path.

### Step 2: Parse & Extract

Read the handoff and extract:
- Objective, approach, current phase
- Decisions with rationale, constraints
- Learnings, gotchas, dead ends, quick wins
- Key files (navigation map)
- UNSPECIFIED items (ask, don't guess)
- Immediate next step

### Step 3: Verify Git State

```bash
git branch --show-current
git status --short
git log --oneline -3
```

Compare with handoff. If diverged — note it, re-read essential files, proceed with current state.

### Step 4: Environment Setup

Run setup commands from handoff if provided. Otherwise check for test scripts, .env, dependencies.

### Step 5: Read Essential Files

From the key files list — read them now. Note any changes since handoff was written.

### Step 6: Present Summary

Brief confirmation of what you absorbed. Include:
- Handoff date, branch, status
- Key decisions (with rationale)
- Gotchas to avoid
- Current state (completed, in progress, remaining)
- UNSPECIFIED items to ask about
- Files loaded
- Immediate next step

Then: **"Awaiting your direction."**

Don't re-explain file contents (they're in context). Don't dump 500 lines. Brief confirmation, then ready to work.

---

## Context Flush

Distill the current session into a plan before starting a clean context.

### Step 1: Analyze and write the plan (while the conversation is still in context)

Read the full conversation. No tool calls — everything is already in context. Write the plan using your host's plan mode if supported, otherwise save it to `tasks/<task>.plan.md` (host mapping: `../_shared/hosts.md`). Use the extraction mindset from the staged process, written directly into the plan structure:

```
# Context: <one-line goal>

## Trajectory
1. Started: <initial goal>
2. <what happened — include dead ends>
3. Current: <where we are>

## Learnings
- <insight, gotcha, dead end with WHY>

## Quick Wins
- <low-effort improvement not yet addressed>

## File Minimap
| File | What's In It | Why It Matters |
|------|-------------|----------------|
| `<absolute path>` | <brief> | <why next session needs it> |

## Working Commands
```bash
# <what it does — ONLY commands verified this session>
<exact command>
```

## User Instructions
<User's actual words. Preserve voice — don't paraphrase.>

## Decisions
- **<decision>**: <rationale> (rejected: <alternatives>)

## Open Questions
- <unresolved>
- <UNSPECIFIED items>

## Next Steps
### Step 1: <action>
- What: <specific>
- Files: <which>
- Done when: <criteria>
```

### Step 2: Start a clean context

Once the plan is saved, clear or open a new session/chat (see `../_shared/hosts.md`) and resume directly from that plan.

### Rules

1. No tool calls during analysis — everything is in context
2. Plan file only — no external files
3. Only verified commands in Working Commands
4. File minimap, not file contents
5. Preserve user voice
6. Skip empty sections
7. Dead ends and trajectory matter — prevent repeating mistakes
