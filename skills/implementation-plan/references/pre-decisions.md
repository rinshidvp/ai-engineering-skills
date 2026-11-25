# Pre-Decisions Reference

## Template

```
Decision: [What needs deciding]
Options: [A, B, C]
Choice: [X]
Rationale: [Why X over others]
```

## Example

```
Decision: Error handling for missing prompt hash
Options:
  A. Return None (graceful degradation)
  B. Raise ValueError (fail fast)
  C. Log warning and skip (partial failure)
Choice: B (Raise ValueError)
Rationale: Learning requires valid prompt. No prompt = invalid state = fail fast.
          User should fix metadata, not get silent failure.
```

## Common Decisions to Make

| Decision | Options | Typical Choice | Rationale |
|----------|---------|----------------|-----------|
| Error handling | Fail fast / Graceful degradation / Partial failure | Fail fast (raise) | Fail fast = correct behavior. Only graceful if business explicitly accepts partial failure. |
| Null handling | Raise exception / Return empty / Return default | Raise exception | Null = unexpected state. Investigate why null, don't guess. |
| Data persistence | Transactional (all-or-nothing) / Eventual | Transactional | Consistency > availability for core data. Eventual only for analytics/cache. |
| Merge strategy | Append / Replace / Merge | Append with separator | Preserve history, simple. Replace loses data. Merge complex. |
| Validation | Strict (fail unknown) / Lenient (ignore) | Strict | Unknown fields = schema drift. Fail early. |
| Migration | Big bang / Gradual rollout | Gradual | Big bang = all-or-nothing risk. Gradual = rollback at any step. |
| Feature flags | Behind flag / Direct deploy | Behind flag | Flag = instant rollback. Direct = PR revert needed. |
| Backwards compat | Break old clients / Support both | Support both (short term) | Break = migration pain. Dual = complexity. Time-box support. |

## When to Add More

Add a pre-decision when:
- Ambiguity would cause different implementations
- Decision affects multiple tasks/components
- Wrong choice = rework or production bug
- You would ask the user anyway during implementation