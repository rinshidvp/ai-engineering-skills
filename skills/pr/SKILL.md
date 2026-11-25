---
name: pr
description: Write a clear, visual Pull Request body with before/after evidence and a Merge Danger assessment (One-Way vs Two-Way Door + Blast Radius). Use when opening or updating a PR, or preparing a branch summary for human review.
---

# Pull Request Summary

Keep prose brief, skip preambles, and use the project's `GLOSSARY.md` terms.
Make it effortless for a human reviewer to judge risk in 10 seconds instead of
reading hundreds of lines blind.

## Template

```markdown
## Summary

<Smallest visual that makes the change obvious: diff-sketch, call tree, file tree, component tree, or Mermaid diagram — plus 1–2 lines of plain English.>

## Evidence

- **Before:** <screenshot, failing test output, or previous behavior>
- **After:** <screenshot, passing test output, or verified command output>

## Merge Danger

- **Door:** `Two-Way` (cheap to roll back) | `One-Way` (hard/destructive to undo — explain why)
- **Blast Radius:** `Low` | `Medium` | `High` — <what could break for users or downstream code>
```

## Rules

1. **Pick the smallest clear visual:** Don't dump all diagram types — pick the
   one view (file diff-sketch, call tree, component tree, or sequence diagram)
   that makes the change click immediately.
2. **Real execution evidence only:**
   - Visual UI changes → before/after screenshots.
   - Logic/API changes → exact test command and passing output (redact any
     secrets with `<REDACTED>`).
3. **Be honest about Merge Danger:**
   - **Two-Way Door + Low Blast Radius:** safe to skim evidence and merge fast.
   - **One-Way Door or High Blast Radius** (migrations, auth, payments, mass
     emails, public API changes): call out exactly what the human reviewer
     should try to break before merging.
