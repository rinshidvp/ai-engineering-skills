# Example Plan: Learning API

**File:** `./tasks/2025-01-15-learning-api.plan.md`

```markdown
# Implementation Plan: Learning API

## Purpose
Add learning endpoint that analyzes human corrections and generates prompt improvement suggestions. Assumes prompts already stored in dataset (via store_prompts=true).

## File Tree
src/decisionengines/
  doc_iq/template/learning/
    models.py (update)
    template_learning_persister.py (new)
  api_server/dociq/
    models.py (new)
  bots/dociq/
    dociq_bot.py (update - add learn method)
test/decisionengines/
  unit_test/doc_iq/template/learning/
    test_template_learning_persister.py (new)
  integration_test/bots/dociq/
    test_learning_flow.py (new)

## Data Models

class LearningPipelineConfig(DeBaseModel):
    """Learning pipeline configuration."""
    prompt_repository: PromptRepository
    template_repository: Optional[TemplateRepository] = None
    persist_to_template: bool = False

class DocIQLearningRequest(DeBaseModel):
    """API request for learning."""
    dataset_id: str
    record_id: str
    prompt_dataset_id: str
    persist_to_template: bool = False

## Orchestration

def learn(dataset_id: str, record_id: str, ...) -> LearningResult:
    """Run learning pipeline on corrected record."""
    # 1. Build dataset source and prompt repository
    # 2. Extract field prompts from dataset schema
    # 3. Build learning config
    # 4. Run RecordLearningPipeline.run()
    # 5. Return result with suggestions

## Boundaries

IN SCOPE:
- Add DociqBot.learn() method
- Create Flask /dociq/learn endpoint
- Create API request/response models

OUT OF SCOPE:
- NOT adding dataset persistence layer
- NOT adding progress callbacks
- NOT adding UI for suggestions (future work)

MUST NOT CHANGE:
- Extraction pipeline config structure
- PromptRepository interface

MUST FOLLOW:
- Use DeBaseModel for all models
- Fail fast on validation errors
- Store prompts in dataset format

## Pre-Decisions

Decision: Error handling for missing prompt hash
Choice: Raise ValueError (fail fast)
Rationale: Learning requires valid prompt. No silent failures.

Decision: Merge strategy for suggestions
Choice: Append with "\n\n" separator
Rationale: Preserve history, simple to implement

## Testing Strategy
- Unit tests for TemplateLearningPersister (mock TemplateRepository)
- Integration test: extraction → review → learn → template updated (end-to-end flow)
- Flask endpoint test via TestClient (verify 200 OK + response structure)

## Verification Checkpoints

| After | Verify |
|-------|--------|
| Models created | `pytest test_models.py` passes |
| Endpoint wired | `curl /dociq/learn` returns 404 (not 500) |
| Full implementation | Integration test passes |

## Acceptance Criteria
- [ ] POST /dociq/learn returns 200 with suggestions
- [ ] Template updated when persist_to_template=true
- [ ] ValueError raised if prompt_hash missing
- [ ] All unit tests pass
- [ ] Integration test passes (full flow)
- [ ] Existing extraction tests still pass (no regressions)

## Tasks (Vertical Tracer-Bullet Slices)

### Task 1: Tracer bullet — run learning pipeline end-to-end (non-persisting)
- **Delivers:** `POST /dociq/learn` accepts a request, validates `prompt_hash`, runs the learning pipeline via `DociqBot.learn()`, and returns 200 with suggestions (models + bot + route + happy-path verification test in one vertical slice).
- **Files:** `src/decisionengines/doc_iq/template/learning/models.py`, `src/decisionengines/api_server/dociq/models.py`, `src/decisionengines/bots/dociq/dociq_bot.py`, `src/decisionengines/api_server/dociq/routes.py`, `test/integration_test/bots/dociq/test_learning_flow.py`
- **Blocked by:** none
- **Agent:** builder
- **Verify:** `pytest test/integration_test/bots/dociq/test_learning_flow.py -k "returns_suggestions" -v` passes

### Task 2: Persist learned prompt additions when `persist_to_template=true`
- **Delivers:** When `persist_to_template=true`, learned instructions append with `"\n\n"` via `TemplateLearningPersister` and persist cleanly without breaking existing extractions.
- **Files:** `src/decisionengines/doc_iq/template/learning/template_learning_persister.py`, `src/decisionengines/bots/dociq/dociq_bot.py`, `test/unit_test/doc_iq/template/learning/test_template_learning_persister.py`, `test/integration_test/bots/dociq/test_learning_flow.py`
- **Blocked by:** Task 1
- **Agent:** builder
- **Verify:** `pytest test/unit_test/doc_iq/template/learning/test_template_learning_persister.py test/integration_test/bots/dociq/test_learning_flow.py -v` passes

### Task 3: Error paths & regression verification
- **Delivers:** Missing `prompt_hash` raises `ValueError` (mapped to 400) and existing extraction suite stays green.
- **Files:** `src/decisionengines/api_server/dociq/routes.py`, `test/integration_test/bots/dociq/test_learning_flow.py`
- **Blocked by:** Task 1
- **Agent:** runner
- **Verify:** Full extraction + learning test suite passes with zero regressions

**Dependency graph:**
```
Task 1 (tracer bullet) ──┬──> Task 2 (persistence slice)
                         └──> Task 3 (error paths & regression)
```
```

---
This example shows all sections fully populated. Copy structure, replace with your feature details.