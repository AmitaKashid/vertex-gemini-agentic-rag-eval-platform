from app.observability.experiment_store import ExperimentStore

HIGHER_IS_BETTER = {"route_accuracy", "retrieval_relevance", "answer_relevance", "faithfulness", "fallback_correctness"}
LOWER_IS_BETTER = {"hallucination_risk", "latency_ms"}

def compare_runs(run_a: str, run_b: str) -> dict:
    store = ExperimentStore()
    a = store.get_run(run_a)
    b = store.get_run(run_b)
    if not a or not b:
        return {"error": "One or both run IDs were not found"}
    comparison = []
    for metric, a_val in a["summary"].items():
        b_val = b["summary"].get(metric)
        if b_val is None:
            continue
        delta = round(b_val - a_val, 4)
        direction = "improved" if ((metric in HIGHER_IS_BETTER and delta > 0) or (metric in LOWER_IS_BETTER and delta < 0)) else "regressed" if delta != 0 else "unchanged"
        comparison.append({"metric": metric, "run_a": a_val, "run_b": b_val, "delta": delta, "direction": direction})
    return {"run_a": run_a, "run_b": run_b, "comparison": comparison}
