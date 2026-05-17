# Evaluation Method

The benchmark runner evaluates each query against expected route, expected source documents, required answer concepts, forbidden answer concepts, verifier output, and latency.

Metrics:

- Route accuracy
- Retrieval relevance
- Answer relevance
- Faithfulness
- Hallucination risk
- Fallback correctness
- Average latency

The goal is not only to measure answer quality, but also to detect regression when changing model provider, prompt version, retrieval settings, and guardrail rules.
