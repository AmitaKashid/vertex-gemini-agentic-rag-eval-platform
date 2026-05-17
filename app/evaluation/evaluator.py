import json, uuid, time
from pathlib import Path
from app.config import settings
from app.schemas import ChatRequest
from app.agent.graph import AgentGraph
from app.evaluation.metrics import score_case, aggregate
from app.observability.experiment_store import ExperimentStore

class EvaluationRunner:
    def __init__(self):
        self.agent = AgentGraph()
        self.store = ExperimentStore()

    def _load_benchmark(self):
        path = Path(settings.benchmark_path)
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def run(self, provider: str = "mock", top_k: int = 3, prompt_version: str = "v1", limit: int | None = None) -> dict:
        run_id = f"run_{uuid.uuid4().hex[:10]}"
        cases = self._load_benchmark()
        if limit:
            cases = cases[:limit]
        started = time.time()
        results = []
        metrics = []
        for case in cases:
            resp = self.agent.run(ChatRequest(query=case["query"], provider=provider, top_k=top_k, prompt_version=prompt_version, conversation_id=f"{run_id}_{case['id']}"))
            pred = resp.model_dump()
            row_metrics = score_case(pred, case)
            metrics.append(row_metrics)
            results.append({"case": case, "prediction": pred, "metrics": row_metrics})
        summary = aggregate(metrics)
        payload = {
            "run_id": run_id,
            "provider": provider,
            "top_k": top_k,
            "prompt_version": prompt_version,
            "case_count": len(cases),
            "started_at": started,
            "summary": summary,
            "results": results,
        }
        self.store.save_run(payload)
        return {"run_id": run_id, "summary": summary, "case_count": len(cases)}
