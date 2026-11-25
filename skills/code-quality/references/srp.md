# SRP Redesign

Clean-slate component analysis. Redesign a target following strict Single Responsibility Principle and KISS principles.

## Analysis

First, determine: does the current implementation violate SRP? Analyze the existing code and identify all different responsibilities and concerns mixed together.

## Redesign Criteria

1. Each component has exactly ONE responsibility
2. Clean abstraction layers — each layer hides complexity from layers above
3. No component knows about other components' internals
4. Simple, focused interfaces
5. Zero backward compatibility — this is clean-slate design

## For Each Proposed Component

Answer:
- What is its SINGLE responsibility? (one sentence)
- What should it NOT know about?
- How would you test it in isolation?

## Implementation Plan Template

```
Components:
- [ComponentName]: [single responsibility, one sentence]
  - Knows: [only its own domain]
  - Does NOT know: [other components, implementation details]
  - Test in isolation by: [approach]

Data flow:
- [Input] → [ComponentA] → [output] → [ComponentB] → [output]

File structure:
- [file]: [what it contains]

Testing strategy:
- [layer]: [how to test without the layers above/below]
```

## Validation

Ask: "If I need to change [concern X], how many components do I touch?"

The answer should be: **exactly one.**

If the answer is more than one, the responsibilities aren't cleanly separated yet.
