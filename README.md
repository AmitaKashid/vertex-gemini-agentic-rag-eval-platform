# Vertex AI and Gemini-Based Agentic RAG Evaluation Platform

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![RAG](https://img.shields.io/badge/RAG-Evaluation%20Platform-purple)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![CI](https://img.shields.io/badge/GitHub%20Actions-CI-black)

A cloud-oriented **Agentic RAG evaluation platform** for comparing local LLM-style inference with Gemini/Vertex AI-style generation across retrieval quality, grounding, hallucination risk, fallback behavior, latency, and regression stability.

The project is designed around a production GenAI question: **how do we know whether a RAG or agentic workflow is safe enough to trust?** Instead of only generating answers, the system records the route decision, retrieved evidence, provider configuration, guardrail outcome, verifier result, latency, and evaluation scores for every run.

---

## Business Problem

Enterprise teams increasingly build RAG systems, AI copilots, and agentic workflows, but many prototypes fail when they move beyond demos because they cannot reliably answer these questions:

- Did the system retrieve the correct evidence?
- Is the final answer grounded in the retrieved context?
- Did the model introduce unsupported claims?
- Should the assistant answer, ask for clarification, or trigger fallback?
- Did a prompt, model, top-k value, or retrieval strategy improve the system or create a regression?
- How does a local model compare with a cloud model such as Gemini under the same benchmark conditions?

This platform addresses those concerns through **structured routing, retrieval evaluation, guardrails, experiment tracking, and repeatable benchmark runs**.

---

## System Overview

```text
User Query / Benchmark Case
        ↓
FastAPI Gateway
        ↓
Query Classifier
        ↓
Agent Router
        ├── direct_answer
        ├── rag_answer
        ├── clarification_needed
        ├── unsupported_fallback
        └── high_risk_fallback
        ↓
Retriever Layer
        ├── Local TF-IDF Retriever
        └── Vector Store Extension Points for FAISS / Qdrant / Vertex AI Vector Search
        ↓
Provider Layer
        ├── Mock Provider for deterministic testing
        ├── Local HTTP Provider for local LLM servers
        └── Gemini Provider for cloud generation
        ↓
Evidence Verifier + Guardrails
        ↓
Trace Logger + Experiment Store
        ↓
Evaluation Reports + Regression Comparison
```

---

## What Makes This Project Different

Most portfolio RAG projects stop at `retrieve context → generate answer`. This project treats RAG as an **evaluated software system**.

The platform stores the operational details needed to debug and improve a real GenAI workflow:

| Capability | Why it matters |
|---|---|
| Provider abstraction | Compares local, mock, and Gemini-style generation without rewriting the pipeline |
| Agentic routing | Decides whether the query needs RAG, fallback, clarification, or high-risk handling |
| Evidence verification | Checks whether the answer is supported by retrieved context before final response release |
| Guardrails | Blocks unsupported, ambiguous, or high-risk responses instead of forcing an answer |
| Experiment tracking | Stores model provider, prompt version, top-k, route, retrieved chunks, metrics, and latency |
| Regression evaluation | Compares repeated benchmark runs to detect prompt, retrieval, or model regressions |
| Cloud mapping | Documents how the local architecture maps to Gemini, Vertex AI Vector Search, and Gen AI evaluation concepts |

---

## Core Features

### Agentic RAG Orchestration

The agent pipeline performs query classification, route selection, retrieval, provider execution, evidence verification, guardrail checks, and response generation. The route is stored with every conversation trace so failures can be analyzed later.

Supported routes:

```text
direct_answer
rag_answer
clarification_needed
unsupported_fallback
high_risk_fallback
```

### Provider Comparison Layer

The system uses a modular provider interface:

```text
LLMProvider
├── MockProvider
├── LocalHTTPProvider
└── GeminiProvider
```

This allows the same benchmark to be executed across multiple generation strategies using the same retriever, prompt version, evaluator, and trace format.

### Retrieval and Evidence Layer

The default implementation uses deterministic local retrieval for reproducible evaluation. The structure includes clean extension points for FAISS, Qdrant, Sentence Transformers, and Vertex AI Vector Search-style backends.

Policy documents included in the repository:

```text
contract_change_policy.md
callback_policy.md
customer_verification_policy.md
escalation_policy.md
invoice_policy.md
complaint_policy.md
```

### Evaluation Engine

The evaluation module scores each benchmark case across:

```text
route_accuracy
retrieval_relevance
answer_relevance
faithfulness
hallucination_risk
fallback_correctness
latency_ms
```

### Observability and Trace Logging

Each conversation trace stores:

```json
{
  "conversation_id": "run_921cb6867a_q_001",
  "query": "What documents are required to change a contract?",
  "route": "rag_answer",
  "provider": "mock",
  "top_k": 3,
  "prompt_version": "v1",
  "retrieved_chunks": [],
  "guardrail_decision": "allowed",
  "verifier": {},
  "latency_ms": 0.1
}
```

---

## Benchmark Results

The repository includes a deterministic benchmark suite covering policy questions, unsupported requests, ambiguous requests, and high-risk prompts. The latest bundled benchmark run was executed with:

```text
provider: mock
top_k: 3
prompt_version: v1
benchmark_cases: 10
unit_tests: 6 passed
```

| Metric | Score |
|---|---:|
| Route accuracy | 80.0% |
| Retrieval relevance | 80.0% |
| Answer relevance | 80.0% |
| Faithfulness | 100.0% |
| Hallucination risk | 10.0% |
| Fallback correctness | 100.0% |
| Mock decision latency | 0.1 ms |

These results are intentionally produced from a deterministic local provider so the benchmark remains reproducible without cloud credentials. Gemini and local LLM runs use the same evaluation interface, but latency and output quality depend on the selected model, endpoint, hardware, and API configuration.

---

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Service health check |
| `POST` | `/chat` | Run one agentic RAG conversation |
| `POST` | `/evaluation/run` | Execute a benchmark run |
| `POST` | `/evaluation/compare` | Compare two stored experiment runs |
| `GET` | `/experiments` | List saved experiment summaries |
| `GET` | `/experiments/{run_id}` | Inspect one evaluation run |
| `GET` | `/traces/{conversation_id}` | Inspect one conversation trace |

---

## Local Setup

### 1. Create environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -e ".[dev]"
```

### 3. Build the retrieval index

```bash
python scripts/ingest_documents.py
```

### 4. Start the API

```bash
uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://localhost:8000/docs
```

---

## Run a Chat Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"What documents are required to change a contract?","provider":"mock","top_k":3,"prompt_version":"v1"}'
```

The response contains the answer, route, retrieved evidence, verifier result, guardrail decision, provider metadata, and latency.

---

## Run Evaluation

```bash
python scripts/run_benchmark.py --provider mock --top-k 3 --prompt-version v1
```

The run is saved under the local experiment store and can be inspected through the API.

---

## Run Tests

```bash
pytest -q
```

Current test status:

```text
6 passed
```

---

## Docker

```bash
docker compose up --build
```

The API is available at:

```text
http://localhost:8000/docs
```

---

## Gemini Configuration

The system runs without cloud credentials in deterministic mock mode. Gemini mode is activated through environment configuration:

```bash
export GEMINI_API_KEY="your_api_key"
export DEFAULT_PROVIDER="gemini"
```

Then execute the benchmark with:

```bash
python scripts/run_benchmark.py --provider gemini --top-k 3 --prompt-version v1
```

The Gemini provider is isolated behind the same interface as local and mock providers, which keeps the orchestration, evaluation, and trace logging consistent across all model backends.

---

## Project Structure

```text
vertex_gemini_agentic_rag_eval_platform/
├── app/
│   ├── api/                 # FastAPI routes
│   ├── agent/               # Classifier, router, guardrails, verifier, graph
│   ├── llm/                 # Mock, local HTTP, and Gemini providers
│   ├── retrieval/           # Retriever and vector-store extension points
│   ├── evaluation/          # Metrics, evaluator, regression comparison, reports
│   ├── observability/       # Trace logging, latency, experiment store
│   └── data/                # Benchmark cases and policy documents
├── scripts/                 # Ingestion, benchmark, comparison, export scripts
├── tests/                   # Unit and API tests
├── docs/                    # Architecture and evaluation documentation
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## Cloud Architecture Mapping

| Local Component | Cloud-Oriented Equivalent |
|---|---|
| `GeminiProvider` | Gemini / Vertex AI model endpoint |
| Retrieval abstraction | Vertex AI Vector Search-style retrieval layer |
| Benchmark runner | GenAI evaluation workflow |
| Experiment store | Evaluation history / model governance store |
| Trace logger | Observability and audit trail layer |
| Guardrails and verifier | Grounding, safety, and response-quality control layer |
| Dockerized FastAPI service | Cloud Run / GKE-style deployable service |

---

## Resume Positioning

```latex
\resumeProjectHeading
{\textbf{Vertex AI and Gemini-Based Agentic RAG Evaluation Platform}}{}
\resumeItemListStart

\resumeItem{Built a \textbf{cloud-oriented GenAI evaluation platform} for comparing local LLM-style inference with Gemini-based generation across RAG answering, agentic routing, grounding quality, hallucination risk, fallback behavior, and latency.}

\resumeItem{Implemented \textbf{agentic RAG orchestration} with FastAPI and modular provider interfaces for query classification, retrieval routing, context injection, evidence verification, fallback handling, and structured response generation.}

\resumeItem{Designed a \textbf{Gemini/Vertex AI provider layer} to evaluate cloud-hosted generation against local model endpoints using shared prompts, retrieval context, trace logging, and benchmark datasets.}

\resumeItem{Built \textbf{RAG evaluation workflows} measuring route accuracy, retrieval relevance, faithfulness, answer relevance, hallucination risk, fallback correctness, provider latency, and regression behavior across repeated runs.}

\resumeItem{Added \textbf{experiment tracking and failure analysis} to compare prompt versions, retrieval settings, top-k values, model providers, and fallback policies, producing reproducible evaluation reports for debugging and model-selection decisions.}

\resumeItem{Prepared a \textbf{cloud-ready deployment and documentation structure} using Docker, environment-based configuration, CI-ready tests, logging, and architecture notes mapping the local system to Gemini, Vertex AI Vector Search, grounding, and GenAI evaluation concepts.}

\resumeItem{\textbf{Technologies Used:} Python, FastAPI, Gemini API, Vertex AI Concepts, RAG, Agentic AI, Prompt Evaluation, RAG Evaluation, Pydantic, Pandas, Scikit-learn, Pytest, Docker, GitHub Actions, Linux, Git}

\resumeItemListEnd
```

---

## Repository Topics

```text
python
fastapi
rag
gemini
vertex-ai
agentic-ai
llm-evaluation
hallucination-detection
retrieval-augmented-generation
prompt-evaluation
docker
pytest
github-actions
```
