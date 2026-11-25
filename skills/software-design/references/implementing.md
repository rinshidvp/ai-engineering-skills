# Implementing with a Design

Read this when building from an existing design.

## Mindset

A design exists. Your job: build what it describes, document contracts in code as you go, flag when reality diverges from blueprint. The design told you what each component *should* guarantee. Implementation is where you discover what it *actually* guarantees and write that down.

End result: every source file has a CONTRACT block a future agent can read without opening DESIGN.md, and DESIGN.md stays in sync with what was actually built.

## Read the design and promote it

1. Check `tasks/` for the design doc (where designs live during creation)
2. Check `<module>/DESIGN.md` if previous implementation already promoted one
3. Check sprint's context.md for contracts and decisions

Understand boundaries before writing code. Honor existing contracts — respect their EXPECTS and rely only on their GUARANTEES.

## Promote the design doc

If design still in `tasks/`, promote it to permanent home before/alongside first implementation commit:

```
project/
├── DESIGN.md                ← system-level: architecture, component relationships
├── auth/
│   ├── DESIGN.md            ← module-level: internal decomposition, interactions
│   ├── pool.py              ← CONTRACT block at top of file
│   └── ...
```

Design doc moves from `tasks/` (proposed) to `<module>/DESIGN.md` (authoritative). Every module with 2+ components gets a DESIGN.md. Project root gets system-level one if design spans multiple modules.

## Write CONTRACT blocks as you code

Every new source file gets a CONTRACT block at the top. You have implementation context — you know what the component actually guarantees. Write the contract while that context is fresh. A separate agent writing it later will produce weaker, less accurate guarantees.

Format:
```python
"""
CONTRACT: ConnectionPool (see auth/DESIGN.md for rationale)

GUARANTEES:
  - Never returns a closed or errored connection
  - All connections returned to pool or closed within timeout_ms
  - Thread-safe without external synchronization
  - At most max_connections open simultaneously

EXPECTS:
  - Caller calls release() when done
  - Config immutable after construction

FAILURE BEHAVIOR:
  - No connection within timeout_ms → TimeoutError, no side effects
  - Connection dies during use → transparent replacement
  - Pool shut down → PoolClosedError on all subsequent acquire()

DOES NOT:
  - Validate SQL or queries
  - Manage transactions
  - Retry failed queries

KNOWN LIMITATIONS:
  - No support for read replicas (returns primary only)
  - No connection draining on graceful shutdown (connections dropped)
"""
```

The CONTRACT block is a promise to future readers. Be specific. If a guarantee is not testable, it is not a guarantee — it is a wish.

## Keep DESIGN.md in sync

If implementation reveals design needs updating:
- Update CONTRACT block in modified source files
- Update module-level DESIGN.md if internal structure changed
- Update system-level DESIGN.md if component relationships changed
- If a GUARANTEE changed, check all callers

A design doc that doesn't match the code actively misleads. Stale docs are worse than no docs.

## Design to fit

When adding to an existing system:
- Follow existing patterns — don't introduce a different pattern without reason
- If existing decomposition makes your feature awkward, boundaries might need to move. Flag as a decision, don't silently hack around it.