import time, uuid
from app.schemas import ChatRequest, ChatResponse, Citation
from app.agent.query_classifier import QueryClassifier
from app.agent.router import AgentRouter
from app.agent.guardrails import GuardrailEngine
from app.agent.response_generator import ResponseGenerator
from app.agent.verifier import EvidenceVerifier
from app.retrieval.retriever import Retriever
from app.observability.trace_logger import TraceLogger

class AgentGraph:
    def __init__(self):
        self.classifier = QueryClassifier()
        self.router = AgentRouter()
        self.guardrails = GuardrailEngine()
        self.generator = ResponseGenerator()
        self.verifier = EvidenceVerifier()
        self.retriever = Retriever()
        self.traces = TraceLogger()

    def run(self, request: ChatRequest) -> ChatResponse:
        start = time.perf_counter()
        conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:12]}"
        route = self.router.route(self.classifier.classify(request.query))
        chunks = self.retriever.retrieve(request.query, top_k=request.top_k) if route.requires_retrieval else []
        guardrail = self.guardrails.check_before_generation(request.query, route, chunks)
        if not guardrail["allowed"]:
            # generator returns safe fallback/clarification for these routes
            result = self.generator.generate(request.query, route, [], request.provider, request.prompt_version)
        else:
            result = self.generator.generate(request.query, route, chunks, request.provider, request.prompt_version)
        verifier = self.verifier.verify(result.answer, chunks) if chunks else {"faithfulness": 1.0, "citation_coverage": 0.0, "hallucination_risk": 0.0, "supported": True}
        latency_ms = int((time.perf_counter() - start) * 1000)
        citations = [Citation(document_id=c.document_id, chunk_id=c.chunk_id, score=c.score, text_preview=c.text[:180]) for c in chunks]
        response = ChatResponse(
            conversation_id=conversation_id,
            answer=result.answer,
            route=route.route,
            provider=result.provider,
            citations=citations,
            verifier=verifier,
            guardrail_decision=guardrail,
            latency_ms=latency_ms,
        )
        self.traces.log({
            "conversation_id": conversation_id,
            "query": request.query,
            "provider": request.provider,
            "prompt_version": request.prompt_version,
            "top_k": request.top_k,
            "route": route.model_dump(),
            "chunks": [c.model_dump() for c in chunks],
            "guardrail": guardrail,
            "answer": result.answer,
            "verifier": verifier,
            "latency_ms": latency_ms,
        })
        return response
