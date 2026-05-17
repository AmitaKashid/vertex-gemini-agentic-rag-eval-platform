import json
from pathlib import Path
from app.config import settings

class ExperimentStore:
    def __init__(self):
        self.root = Path(settings.experiment_dir)
        self.root.mkdir(parents=True, exist_ok=True)

    def save_run(self, payload: dict) -> None:
        path = self.root / f"{payload['run_id']}.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def get_run(self, run_id: str) -> dict | None:
        path = self.root / f"{run_id}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def list_runs(self) -> list[dict]:
        runs = []
        for path in sorted(self.root.glob("run_*.json"), reverse=True):
            data = json.loads(path.read_text(encoding="utf-8"))
            runs.append({"run_id": data["run_id"], "provider": data["provider"], "top_k": data["top_k"], "prompt_version": data["prompt_version"], "case_count": data["case_count"], "summary": data["summary"]})
        return runs
