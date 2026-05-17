from fastapi import FastAPI
from app.api.routes_chat import router as chat_router
from app.api.routes_evaluation import router as eval_router
from app.api.routes_experiments import router as exp_router
from app.api.routes_traces import router as trace_router
from app.api.routes_health import router as health_router

app = FastAPI(
    title="Vertex AI and Gemini-Based Agentic RAG Evaluation Platform",
    version="0.1.0",
    description="Agentic RAG evaluation platform with provider comparison, guardrails, traces, and regression testing.",
)

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(eval_router)
app.include_router(exp_router)
app.include_router(trace_router)
