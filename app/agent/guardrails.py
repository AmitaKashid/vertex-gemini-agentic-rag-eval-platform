from app.schemas import RoutingDecision, RetrievedChunk

class GuardrailEngine:
    def check_before_generation(self, query: str, route: RoutingDecision, chunks: list[RetrievedChunk]) -> dict:
        if route.route == "clarification_needed":
            return {"allowed": False, "reason": "clarification_required", "next_action": "ask_user_clarifying_question"}
        if route.route == "unsupported_fallback":
            return {"allowed": False, "reason": "unsupported_domain", "next_action": "fallback"}
        if route.route == "high_risk_fallback":
            return {"allowed": False, "reason": "high_risk_request", "next_action": "safe_fallback"}
        if route.requires_retrieval and not chunks:
            return {"allowed": False, "reason": "no_retrieval_evidence", "next_action": "fallback"}
        if route.requires_retrieval and chunks and max(c.score for c in chunks) < 0.05:
            return {"allowed": False, "reason": "low_retrieval_confidence", "next_action": "fallback"}
        return {"allowed": True, "reason": "passed", "next_action": "generate"}
