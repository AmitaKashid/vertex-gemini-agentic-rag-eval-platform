import re
from app.llm.base import LLMProvider
from app.schemas import ProviderResult

class MockProvider(LLMProvider):
    name = "mock"
    model = "deterministic-rag-mock"

    def generate(self, prompt: str, context: list[str], metadata: dict) -> ProviderResult:
        if context:
            combined = " ".join(context)
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", combined) if s.strip()]
            answer = " ".join(sentences[:3])
            answer = f"Based on the retrieved policy evidence, {answer}"
        else:
            answer = "I can help evaluate RAG behavior, compare providers, and inspect traces for enterprise GenAI workflows."
        return ProviderResult(answer=answer, provider=self.name, model=self.model, raw={"mode": "offline_deterministic"})
