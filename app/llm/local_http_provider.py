import httpx
from app.config import settings
from app.llm.base import LLMProvider
from app.schemas import ProviderResult

class LocalHttpProvider(LLMProvider):
    name = "local_http"
    model = "openai-compatible-local-llm"

    def generate(self, prompt: str, context: list[str], metadata: dict) -> ProviderResult:
        payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}
        try:
            response = httpx.post(settings.local_llm_base_url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return ProviderResult(answer=answer or "Local model returned an empty response.", provider=self.name, model=self.model, raw=data)
        except Exception as exc:
            return ProviderResult(answer=f"Local provider unavailable: {exc}. Falling back to safe response: evidence was retrieved but generation could not complete.", provider=self.name, model=self.model, raw={"error": str(exc)})
