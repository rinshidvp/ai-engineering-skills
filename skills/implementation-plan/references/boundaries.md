# Boundaries Reference

## The Box: Defining Boundaries

Every plan defines these boundaries, so the implementer knows what it may and may not touch:

### IN SCOPE
Explicit list of what you WILL implement.

Example:
- Add `update_template()` to TemplateRepository interface
- Create TemplateLearningPersister class for merging suggestions
- Add `learn()` method to DociqBot
- Create Flask `/dociq/learn` endpoint

### OUT OF SCOPE
Explicit list of what you WILL NOT do.

Example:
- NOT changing extraction pipeline config structure
- NOT adding dataset persistence layer
- NOT implementing dry-run mode (future work)

### MUST NOT CHANGE
Existing code that's off-limits.

Example:
- Extraction pipeline configuration (already works, leave untouched)
- PromptDoc structure (used by other systems)
- Existing template schema fields (only adding to learnings field)

### MUST FOLLOW
Patterns/conventions that are mandatory.

Example:
- Use DeBaseModel for all data models
- Use DatasetSource abstraction (not direct DB calls)
- Follow existing error handling pattern (fail fast, no try/except without justification)
- Store prompts in dataset format (not filesystem)

## BOUNDARY SANITY CHECK

Before finalizing the plan, ask:

- **Am I solving a symptom or the root cause?** If you're adding a lookup/workaround to connect things, is that because an abstraction is missing upstream?
- **Would this plan make the code cleaner or messier?** If messier, consider whether refactoring is the real solution.
- **Does the plan cut around concepts or through them?** Data that belongs together should stay together. Components should have single responsibilities.

If the answer to any of these is "messier" or "through" — pause. Ask:
*"I'm planning to add X here, but I notice it's working around existing structure. Should we refactor Y instead?"*

The human has context about why things are structured the way they are. Use it.