import json
from pathlib import Path
from app.config import settings

class TraceLogger:
    def __init__(self):
        self.trace_dir = Path(settings.trace_dir)
        self.trace_dir.mkdir(parents=True, exist_ok=True)

    def log(self, trace: dict) -> None:
        path = self.trace_dir / f"{trace['conversation_id']}.json"
        path.write_text(json.dumps(trace, indent=2), encoding="utf-8")

    def get_trace(self, conversation_id: str) -> dict | None:
        path = self.trace_dir / f"{conversation_id}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))
