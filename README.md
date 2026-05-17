# Vertex AI and Gemini-Based Agentic RAG Evaluation Platform

A production-style portfolio project for evaluating **local LLM vs Gemini/Vertex-style RAG and agentic workflows** across retrieval quality, grounding, hallucination risk, fallback behavior, latency, and regression performance.

Most RAG demos stop after returning an answer. This project focuses on the harder enterprise problem: **deciding whether the answer should be trusted**, whether the right evidence was retrieved, whether the model hallucinated, whether fallback should trigger, and whether a new prompt/model/retrieval configuration improves or regresses system behavior.

## Key Features

- FastAPI backend with `/chat`, `/evaluation/run`, `/evaluation/compare`, `/experiments`, `/traces`, and `/health` endpoints.
- Modular provider layer supporting `mock`, `local_http`, and `gemini` providers.
- Agentic routing for direct answer, RAG answer, clarification, unsupported fallback, and high-risk fallback.
- Retrieval layer over policy documents with deterministic TF-IDF retrieval by default, with clean extension points for FAISS/Qdrant/Sentence Transformers.
- Evidence verification and guardrail checks before final answer release.
- Evaluation engine with benchmark dataset and metrics for intent/route accuracy, retrieval relevance, answer relevance, faithfulness, hallucination risk, fallback correctness, and latency.
- Experiment tracking with JSONL traces and repeatable run comparison.
- Docker, GitHub Actions, tests, documentation, and recruiter-ready project structure.

## Architecture

```text
User Query / Benchmark Query
        ↓
FastAPI Gateway
        ↓
Query Classifier
        ↓
Agent Router
        ├── direct_answer
        ├── rag_answer
        ├── clarification_needed
        └── unsupported_fallback
        ↓
Retriever Layer
        ├── Local TF-IDF Retriever
        └── Vector Store Extension Point
        ↓
Provider Layer
        ├── Mock Provider
        ├── Local OpenAI-Compatible Provider
        └── Gemini Provider
        ↓
Evidence Verifier + Guardrails
        ↓
Trace Logger + Experiment Store
        ↓
Evaluation Reports
```

## Why This Is Not a Basic RAG App

This project treats RAG as an evaluated system, not just a prompt. Each run stores model provider, prompt version, retrieval top-k, route decision, retrieved chunks, verifier result, final answer, latency, and evaluation metrics. This allows regression comparisons such as:

- Gemini vs local LLM provider
- top-k=3 vs top-k=5
- prompt v1 vs prompt v2
- direct RAG vs agentic routing
- fallback enabled vs fallback disabled

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python scripts/ingest_documents.py
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

Try a chat request:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"What documents are required to change a contract?","provider":"mock","top_k":3}'
```

Run benchmark evaluation:

```bash
python scripts/run_benchmark.py --provider mock --top-k 3 --prompt-version v1
```

Compare two runs:

```bash
python scripts/compare_runs.py --run-a <RUN_ID_A> --run-b <RUN_ID_B>
```

## Gemini Setup

The project runs fully in mock mode by default. For Gemini mode, set:

```bash
export GEMINI_API_KEY="your-key"
export DEFAULT_PROVIDER="gemini"
```

Then call:

```bash
python scripts/run_benchmark.py --provider gemini --top-k 3
```

The provider layer is isolated so the system remains testable even when cloud credentials are unavailable.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health check |
| POST | `/chat` | Run one agentic RAG conversation |
| POST | `/evaluation/run` | Run benchmark evaluation |
| POST | `/evaluation/compare` | Compare two experiment runs |
| GET | `/experiments` | List stored experiment summaries |
| GET | `/experiments/{run_id}` | Inspect one experiment |
| GET | `/traces/{conversation_id}` | Inspect one conversation trace |

## Example Evaluation Output

```text
Metric                      Value
route_accuracy              0.91
retrieval_relevance         0.84
answer_relevance            0.88
faithfulness                0.86
hallucination_risk          0.10
fallback_correctness        0.93
avg_latency_ms              640
```

Use real results after running the benchmark on your machine.

## Resume Mapping

```latex
\resumeProjectHeading
{\textbf{Vertex AI and Gemini-Based Agentic RAG Evaluation Platform}}{}
\resumeItemListStart
\resumeItem{Built a \textbf{cloud-oriented GenAI evaluation platform} for comparing local LLM inference with Gemini-based generation across RAG answering, agentic routing, grounding quality, hallucination risk, and latency.}
\resumeItem{Implemented \textbf{agentic RAG orchestration} with FastAPI and modular provider interfaces for query classification, retrieval routing, context injection, evidence verification, fallback handling, and structured response generation.}
\resumeItem{Built \textbf{RAG evaluation workflows} measuring context precision, retrieval relevance, faithfulness, answer relevance, citation coverage, hallucination risk, fallback correctness, provider latency, and regression behavior across repeated runs.}
\resumeItem{Added \textbf{experiment tracking and failure analysis} to compare prompt versions, retrieval settings, top-k values, model providers, and fallback policies, producing reproducible evaluation reports for debugging and model-selection decisions.}
\resumeItem{\textbf{Technologies Used:} Python, FastAPI, Gemini API, Vertex AI Concepts, Sentence Transformers/Vector Search Concepts, RAG, Agentic AI, Prompt Evaluation, Pydantic, Pandas, Pytest, Docker, GitHub Actions, Linux, Git}
\resumeItemListEnd
```

## Repository Topics

`python`, `fastapi`, `rag`, `gemini`, `vertex-ai`, `agentic-ai`, `llm-evaluation`, `hallucination-detection`, `retrieval-augmented-generation`, `docker`, `pytest`
