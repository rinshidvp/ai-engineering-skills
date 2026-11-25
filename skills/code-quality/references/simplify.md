# Simplification

A behavior-preserving clarity pass. Not a rewrite. Not a refactor. Making code clearer without changing what it does.

## The One Rule

**Never change what the code does.** Every input produces the same output. Every side effect fires the same way. Every error propagates the same path. If you're unsure whether a change preserves behavior, don't make it.

## Find the Changed Code

1. Run `git diff --name-only` for unstaged changes
2. Run `git diff --cached --name-only` for staged changes
3. If nothing is dirty, run `git diff HEAD~1 --name-only` for the last commit
4. If the user specifies files or scope (task arguments / explicit file list), use that instead

Read every changed file. Understand it fully before touching anything.

## What to Simplify

**Unnecessary complexity:**
- Nested conditionals that could be early returns or guard clauses
- Boolean expressions that could be simplified (`if x == True` → `if x`)
- Redundant variables assigned and immediately returned
- Double negations (`not (not x and not y)` → `x or y`)
- Overly defensive code — null checks on values that can't be null

**Redundancy:**
- Dead code — unreachable branches, unused imports, commented-out blocks
- Duplicate logic appearing in multiple places within the changed files
- Wrapper functions that just delegate with the same signature
- Abstractions with only one use that don't clarify intent

**Unclear naming:**
- Variables named `data`, `result`, `temp`, `val` when a domain term exists
- Functions whose names don't describe what they actually do
- Inconsistent naming within the same file

**Structural noise:**
- Overly granular functions that fragment a simple, linear operation
- Classes that exist for one method (where a function would do)
- Unnecessary intermediate data structures
- Verbose patterns where the language offers a clearer idiom

**Comments that lie or add nothing:**
- Comments restating the code (`# increment counter` above `counter += 1`)
- Stale comments describing what the code *used to* do
- Addressed TODO/FIXME that were never removed

## What NOT to Simplify

- **Working abstractions that aid understanding.** A well-named helper function is simpler even if inlining it saves lines.
- **Error handling.** Don't remove catches, guards, or validation just because the happy path works.
- **Intentional verbosity.** A clear `if/elif/else` chain sometimes beats clever dictionary dispatch.
- **Code outside the change scope.** Unless the user specifies otherwise, stay in recently modified files.
- **Tests.** Test verbosity is often intentional — it makes failures easier to diagnose.

## 5-Step Process

1. **Read first, completely.** Read every changed file end to end. Understand the flow, conventions, patterns already in use.
2. **Respect the project's voice.** Match naming patterns, indentation, comment density — whatever's already there. Consistency is its own form of simplicity.
3. **Make changes that pass the "obviously better" test.** If a change requires explanation for why it's simpler, it probably isn't.
4. **Prefer small, independent changes.** Don't restructure a whole function at once. Each edit should be self-contained, easy to review, easy to revert.
5. **Show what you changed and why.** Brief summary grouped by type (removed dead code, simplified conditionals, improved naming). The diff is the real documentation.

## The Balance

Clear and concise, but never cryptic.

- Replacing 5 readable lines with 1 dense line → compression, not simplification
- Replacing 1 dense line with 5 readable lines → might be simplification
- If a pattern is "clever," it's probably not simple
- If you have to think about whether a change is clearer, it's probably not worth making

When done, list changes made grouped by category. If you made no changes, say so — sometimes code is already as simple as it should be. That's a valid outcome.
