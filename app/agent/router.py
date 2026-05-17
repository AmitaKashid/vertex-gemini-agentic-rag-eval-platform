from app.schemas import RoutingDecision

class AgentRouter:
    def route(self, decision: RoutingDecision) -> RoutingDecision:
        # This class is intentionally separate to make future LangGraph routing easy.
        return decision
