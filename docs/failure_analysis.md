# Failure Analysis

Common failure categories:

- Wrong route: classifier selected direct answer instead of RAG.
- Low retrieval relevance: retrieved source does not match expected source.
- Unsupported claim: answer includes details not found in context.
- Over-fallback: system asks clarification when evidence was sufficient.
- Under-fallback: system answers when it should have declined or escalated.

For each benchmark run, inspect the stored JSON file under `.runs/` and traces under `.runs/traces/`.
