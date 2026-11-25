# Commitment Template

Copy when brainstorm lands. Omit irrelevant lines, never hide material assumption.

```
Decision:     [what we decided]
Considered:   [serious paths]
Chosen:       [path]
Why:          [constraint/evidence/tradeoff tipping it]
Assumptions:  [material assumptions carrying choice]
Limitations:  [what this does not handle]
Fine because: [why limits fit now]
Reversal:     [observable condition reopening decision]
```

Done when: decision + success clear, strongest alternative tested, assumptions visible, main failure considered, scope kept, reversal known, cheap decisive investigation done.

Write to decision log if exists. If the decision passes the 3-part ADR filter in `domain-modeling.md` (hard to reverse + surprising without context + real trade-off), also save a concise ADR in `docs/adr/NNNN-slug.md` including the `Reversal` condition so future sessions know when the decision expires.
Hand to software-design / implementation-plan only when mature.
