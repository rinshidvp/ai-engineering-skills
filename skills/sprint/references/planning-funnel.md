# Planning Funnel

Upstream phases that run before brick decomposition. Each phase has a checkpoint — stop, present the deliverable, get explicit approval before proceeding.

---

## When to Use Upstream Planning

The sprint's input assessment determines which phases apply. The funnel is not mandatory — it scales to the work.

| Feature Size | Upstream Phases |
|--------------|-----------------|
| Small (1-2 files, no unknowns) | Reuse Discovery → decompose |
| Small (1-2 files, with unknowns) | Reuse Discovery → Discovery → decompose |
| Medium (3-5 files) | Reuse Discovery → Design → Implementation Plan → decompose |
| Large (5+ files, multi-component) | Reuse Discovery → Spec → QA Plan → Design → Implementation Plan → decompose |
| Fuzzy idea (any size) | Brainstorm → Reuse Discovery → then scale by size above |

Reuse Discovery and Specification Grounding always run, regardless of size (see `creating-a-sprint.md`). Implementation Planning always runs for multi-file features. Start minimal on everything else.

---

## Entry Points

**Fuzzy idea** ("I want to add caching", "can we improve X"):
1. Start at Brainstorming
2. Refine through dialogue
3. Then scale by complexity (small → plan, medium → design + plan, large → full funnel)

**Clear scope, no unknowns** ("implement retry logic on the payment client"):
1. Assess complexity
2. Start at appropriate phase per scaling guidance
3. Follow phases sequentially with checkpoints

**User provides spec:**
1. Start at QA Planning or Design
2. User already did the requirements phase

**User provides design:**
1. Start at Implementation Planning
2. User already did phases 1-3

**User provides plan:**
1. Start at brick decomposition
2. User already did all upstream phases

---

## Phase Details

### Discovery

**Skill:** `discovery` (in-repo at `skills/discovery/SKILL.md` — merged grill-me + brainstorming).

**When to use:**
- Idea is vague or fuzzy ("I want to add caching")
- Multiple interpretations are possible
- You're not sure what they actually want
- Need to explore alternatives before committing

**When to skip:**
- Requirements already clear and specific
- User provides a detailed spec
- Simple, well-defined task with obvious scope

**Process:**
1. Scout the codebase first — send an Explore agent to find relevant files, patterns, similar code
2. Read the files that matter (don't work from summaries — understand the code)
3. Share what you found: existing patterns, integration points, similar code
4. Ask clarifying questions one at a time — natural text, not form fields
5. Explore 2-3 approaches with tradeoffs, informed by real understanding
6. Nail down scope, constraints, success criteria
7. Confirm direction before moving on

**Output:** Refined idea ready for next phase

**Checkpoint questions:**
- [ ] Problem clearly understood?
- [ ] Approach chosen from alternatives?
- [ ] Scope defined (in/out)?
- [ ] Success criteria clear?
- [ ] Ready to move to spec/design/plan?

**Approval looks like:** "Yes that's what I want", "Let's go with approach A", "Scope looks right"

---

### Requirements

**Skill:** _spec_ (optional, not in this repo — follow the process below inline).

**When to use:**
- External stakeholder requirements
- Multiple interpretations possible
- Need alignment before design investment

**When to skip:**
- Requirements already crystal clear (from ticket, prior discussion)
- Internal tooling with obvious scope
- User provides a complete spec

**Output:** `./tasks/YYYY-MM-DD-<title>.spec.md`

**Checkpoint questions:**
- [ ] Problem statement: WHO feels pain, WHY now?
- [ ] User stories: Jobs-to-be-done identified?
- [ ] Acceptance criteria: All testable (pass/fail)?
- [ ] Requirements prioritized (MUST/SHOULD/COULD)?
- [ ] Out of scope: Explicit exclusions?

**Approval looks like:** "Spec approved", "Requirements look good", "Proceed to QA plan"

---

### QA Planning

**Skill:** _qa-plan_ (optional, not in this repo — follow the process below inline).

**When to use:**
- Feature has multiple behaviors to verify
- Integration with external systems
- User acceptance criteria need test mapping

**When to skip:**
- Trivial feature with obvious test cases
- Pure refactoring (behavior unchanged)

**Output:** `./tasks/YYYY-MM-DD-<title>.qa-plan.md`

**Checkpoint questions:**
- [ ] Every MUST requirement has a test case?
- [ ] Edge cases identified?
- [ ] Integration points tested?
- [ ] Test data requirements documented?

**Approval looks like:** "QA plan approved", "Test cases cover everything", "Proceed to design"

---

### Design

**Skill:** `software-design` (in this repo at `skills/software-design/SKILL.md`).

**When to use:**
- Feature touches multiple components or layers
- New abstractions or contracts need to be defined
- Architectural decisions affect more than one brick
- Whenever bricks would otherwise be invented from intuition rather than derived from contracts

For sprint-scale work, this is the default. Skip only for single-component changes or pure refactors with established patterns.

**When to skip:**
- Single-component change inside an existing module with a clear pattern
- Prototype/throwaway code

**Output:** `./tasks/YYYY-MM-DD-<title>.design.md` — components, layers, and GUARANTEES / EXPECTS / FAILURE BEHAVIOR per component.

**Checkpoint questions:**
- [ ] Components named with explicit GUARANTEES, EXPECTS, FAILURE BEHAVIOR?
- [ ] Layers identified — each one exposing a higher-level abstraction to what's above?
- [ ] Right altitude — no layer leaks complexity upward, no layer becomes lossy?
- [ ] Goals measurable, non-goals explicit?
- [ ] Assumptions listed with validation methods (spike or closing brick)?
- [ ] Major decisions have options + rationale?
- [ ] One-way doors identified and justified?
- [ ] Testability addressed — is every component independently verifiable?
- [ ] Blast radius analyzed?

**Approval looks like:** "Design approved", "Layers look right", "Proceed to planning"

**The design MUST be validated by the user before brick decomposition begins.** Component layers, abstractions, and contracts are load-bearing — getting them wrong upfront cascades into every brick. Present the design.md, ask for approval, wait. No exceptions.

Brick boundaries are derived from the design's contracts. A brick that can't reference a guarantee from the design is either too high in the tree or working from a missing design.

---

### Implementation Planning

**Skill:** `implementation-plan` (in this repo at `skills/implementation-plan/SKILL.md`).

**When to skip:** Never skip for multi-file features.

**Output:** `./tasks/YYYY-MM-DD-<title>.plan.md`

**Checkpoint questions:**
- [ ] Data models fully specified (fields, types)?
- [ ] API contracts defined (signatures, return types)?
- [ ] Orchestration flow clear (A → B → C)?
- [ ] Boundaries set (IN/OUT scope, MUST NOT CHANGE)?
- [ ] Pre-decisions made with rationale?
- [ ] Testing strategy specified?
- [ ] Verification checkpoints defined?

**Approval looks like:** "Plan approved", "Ready to implement", "Go ahead"

---

## Review Checkpoint Protocol

At every checkpoint:

1. STOP implementation
2. PRESENT deliverable to user:
   - File location
   - Brief summary (5-10 lines max)
   - Key decisions made
3. ASK checkpoint-specific questions ("Requirements clear? Scope agreed?")
4. WAIT for explicit approval ("proceed", "go ahead", "approved", "yes, use option B")
5. If changes requested: incorporate, re-present, wait again
6. Only after approval: proceed to next phase

NEVER skip checkpoints. User must explicitly approve each phase.

---

## Testing Anti-Patterns to Avoid

These apply during implementation, not just planning — but the QA plan is where you catch them early.

**Over-mocking:**
```python
# Wrong: Mock the database, mock the service, mock the validator, test that mock was called
mock_db = Mock()
mock_service = Mock()

# Right: Use real validator, real service logic, mock only external APIs
real_validator = Validator()
service = Service(api=mock_external_api)  # Only external boundary mocked
result = service.process(input)
assert result.is_valid  # Test real behavior
```

**Testing implementation, not behavior:**
```python
# Wrong: Assert that internal method X was called with Y
service.process(data)
service._internal_helper.assert_called_with(data)

# Right: Assert that user-visible outcome Z occurred
result = service.process(data)
assert result.status == "completed"
assert len(result.items) == 3
```

**Tests that can't fail:**
```python
# Wrong: Mock returns expected value, assert expected value was returned
mock.get_data.return_value = {"key": "value"}
result = processor.process(mock)
assert result == {"key": "value"}  # Circular, tests nothing

# Right: Test that exercises real logic with real assertions
result = processor.process(real_data)
assert result.transformed_key == expected_transformation
```

**Skipping hard-to-test components:**
If it's hard to test, redesign for testability: add dependency injection, extract pure functions, create interfaces for boundaries. "I'll test it manually" is not a plan.

**The mock infection:** If you need 4+ mocks, your design needs work. Mock boundaries (external APIs, clock), test internals with real code.

---

## Skills Reference

| Phase | Skill | Output | Location |
|-------|-------|--------|----------|
| Discovery | `discovery` | `*.requirements.md` + direction | in-repo: `skills/discovery/SKILL.md` |
| Requirements | _spec_ | `*.spec.md` | optional — inline process above |
| QA Planning | _qa-plan_ | `*.qa-plan.md` | optional — inline process above |
| Design | `software-design` | `*.design.md` | in-repo: `skills/software-design/SKILL.md` |
| Implementation Planning | `implementation-plan` | `*.plan.md` | in-repo: `skills/implementation-plan/SKILL.md` |
| Debug recovery | `debugging` | root cause + fix | in-repo: `skills/debugging/SKILL.md` |
| Test discipline | `writing-unit-tests` | feature verification | in-repo: `skills/writing-unit-tests/SKILL.md` |

Skill locations in this repo: `skills/<skill-name>/SKILL.md`. After
`install.ps1`, they are installed side by side in each host's global skills
folder, so relative paths like `../../software-design/SKILL.md` resolve there too.
