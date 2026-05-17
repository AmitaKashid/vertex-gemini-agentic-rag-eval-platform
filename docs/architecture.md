# Architecture

The platform is built around a modular agentic RAG pipeline:

1. FastAPI receives a user or benchmark query.
2. Query classifier predicts the route.
3. Agent router selects direct answer, RAG answer, clarification, or fallback.
4. Retriever collects evidence from policy documents.
5. Provider layer generates an answer using mock/local/Gemini provider.
6. Verifier checks whether the answer is supported by retrieved evidence.
7. Trace logger stores route, chunks, guardrails, response, verifier output, and latency.
8. Evaluator aggregates benchmark metrics and stores experiment runs.

This structure maps cleanly to Vertex AI concepts: Gemini as the generation provider, Vertex AI Vector Search as the retrieval backend, and Gen AI Evaluation as the evaluation layer.
