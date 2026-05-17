from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    app_env: str = "local"
    default_provider: str = "mock"
    gemini_api_key: str | None = None
    local_llm_base_url: str = "http://localhost:8000/v1/chat/completions"
    experiment_dir: Path = Path(".runs")
    trace_dir: Path = Path(".runs/traces")
    document_dir: Path = Path("app/data/documents")
    benchmark_path: Path = Path("app/data/benchmark_questions.jsonl")

    class Config:
        env_file = ".env"

settings = Settings()
settings.experiment_dir.mkdir(parents=True, exist_ok=True)
settings.trace_dir.mkdir(parents=True, exist_ok=True)
