import re
from statistics import mean

def token_set(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9]{3,}", text.lower()))

def contains_any(text: str, terms: list[str]) -> bool:
    t = text.lower()
    return any(term.lower() in t for term in terms)

def score_case(pred: dict, gold: dict) -> dict:
    expected_route = gold.get("expected_route")
    route_accuracy = 1.0 if pred.get("route") == expected_route else 0.0
    expected_sources = set(gold.get("expected_sources", []))
    retrieved_sources = {c.get("document_id") for c in pred.get("citations", [])}
    retrieval_relevance = len(expected_sources & retrieved_sources) / max(len(expected_sources), 1) if expected_sources else 1.0
    must = gold.get("must_contain", [])
    should_not = gold.get("should_not_contain", [])
    answer = pred.get("answer", "")
    answer_relevance = sum(1 for m in must if m.lower() in answer.lower()) / max(len(must), 1) if must else 1.0
    hallucination_flags = sum(1 for s in should_not if s.lower() in answer.lower())
    hallucination_risk = min(1.0, hallucination_flags / max(len(should_not), 1)) if should_not else pred.get("verifier", {}).get("hallucination_risk", 0.0)
    fallback_expected = expected_route in {"unsupported_fallback", "clarification_needed", "high_risk_fallback"}
    fallback_correctness = 1.0 if (fallback_expected and pred.get("route") == expected_route) or (not fallback_expected and pred.get("route") not in {"unsupported_fallback", "clarification_needed", "high_risk_fallback"}) else 0.0
    return {
        "route_accuracy": route_accuracy,
        "retrieval_relevance": retrieval_relevance,
        "answer_relevance": answer_relevance,
        "faithfulness": float(pred.get("verifier", {}).get("faithfulness", 0.0)),
        "hallucination_risk": hallucination_risk,
        "fallback_correctness": fallback_correctness,
        "latency_ms": float(pred.get("latency_ms", 0)),
    }

def aggregate(rows: list[dict]) -> dict:
    keys = rows[0].keys() if rows else []
    return {k: round(mean(r[k] for r in rows), 4) for k in keys}
