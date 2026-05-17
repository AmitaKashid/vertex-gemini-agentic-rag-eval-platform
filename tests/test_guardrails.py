from app.agent.guardrails import GuardrailEngine
from app.schemas import RoutingDecision

def test_guardrail_blocks_unsupported():
    route = RoutingDecision(route="unsupported_fallback", confidence=0.9, reason="x")
    result = GuardrailEngine().check_before_generation("weather", route, [])
    assert result["allowed"] is False
