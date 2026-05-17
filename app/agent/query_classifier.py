from app.schemas import RoutingDecision

class QueryClassifier:
    """Deterministic classifier for reproducible portfolio evaluation.

    This can be replaced with an LLM classifier, but deterministic rules are useful for tests,
    benchmark repeatability, and explaining failure cases.
    """

    unsupported_terms = {"weather", "stock", "football", "medical diagnosis", "legal advice"}
    high_risk_terms = {"guarantee", "always", "definitely", "legal", "diagnose", "delete all"}
    ambiguous_terms = {"it", "this", "that", "help me", "problem"}

    def classify(self, query: str) -> RoutingDecision:
        q = query.lower().strip()
        if any(term in q for term in self.unsupported_terms):
            return RoutingDecision(route="unsupported_fallback", confidence=0.92, reason="Out-of-domain request")
        if len(q.split()) < 4 or q in self.ambiguous_terms:
            return RoutingDecision(route="clarification_needed", confidence=0.75, reason="Query is too ambiguous")
        if any(term in q for term in self.high_risk_terms):
            return RoutingDecision(route="high_risk_fallback", confidence=0.88, reason="Potentially high-risk claim/action")
        if any(term in q for term in ["policy", "documents", "required", "contract", "invoice", "callback", "escalation", "verification", "complaint"]):
            return RoutingDecision(route="rag_answer", confidence=0.9, reason="Document-grounded answer required", requires_retrieval=True)
        return RoutingDecision(route="direct_answer", confidence=0.72, reason="General platform question")
