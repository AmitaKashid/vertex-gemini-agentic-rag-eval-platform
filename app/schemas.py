from typing import Any, Literal
from pydantic import BaseModel, Field

RouteName = Literal[
    "direct_answer",
    "rag_answer",
    "clarification_needed",
    "unsupported_fallback",
    "high_risk_fallback",
]

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=2)
    provider: str = "mock"
    top_k: int = Field(default=3, ge=1, le=10)
    prompt_version: str = "v1"
    conversation_id: str | None = None

class Citation(BaseModel):
    document_id: str
    chunk_id: str
    score: float
    text_preview: str

class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    route: RouteName
    provider: str
    citations: list[Citation] = []
    verifier: dict[str, Any]
    guardrail_decision: dict[str, Any]
    latency_ms: int

class RoutingDecision(BaseModel):
    route: RouteName
    confidence: float
    reason: str
    requires_retrieval: bool = False
    fallback_allowed: bool = True

class RetrievedChunk(BaseModel):
    document_id: str
    chunk_id: str
    score: float
    text: str

class ProviderResult(BaseModel):
    answer: str
    provider: str
    model: str
    raw: dict[str, Any] = {}

class EvaluationRunRequest(BaseModel):
    provider: str = "mock"
    top_k: int = 3
    prompt_version: str = "v1"
    limit: int | None = None

class CompareRunsRequest(BaseModel):
    run_a: str
    run_b: str
