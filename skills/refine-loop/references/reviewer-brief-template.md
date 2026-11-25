# Reviewer Brief Template

Copy-paste, fill brackets. Give context not judgment.

```
Review [feature/artifact] — [lens skill] review.

Scope:
- Files: [paths, branch or worktree]
- Does: [1 sentence what it does]

Apply: read and apply [skill names] before reviewing.
Context: goal [X], users [Y], scale [Z], criticality [low/med/high].
Depth: [real bugs only | + structural]. Budget 1 pass.

Report ranked by severity with file:line + why + minimal fix.
Permission to say clean — don't manufacture findings.
```

Do NOT include:
- Suspected defects, hypotheses, "check whether X"
- Your quality assessment
- Leading checklists ("focus on correctness, edge cases and...")

Bad: "Check empty-scopes edge, verify useEffect cleanup, confirm narrowing fix."
Good: brief above composed fresh — reviewer forms own opinion.
