from app.config import settings
from app.llm.base import LLMProvider
from app.schemas import ProviderResult

class GeminiProvider(LLMProvider):
    name = "gemini"
    model = "gemini-1.5-flash-or-configured"

    def generate(self, prompt: str, context: list[str], metadata: dict) -> ProviderResult:
        if not settings.gemini_api_key:
            return ProviderResult(
                answer="Gemini provider is configured, but GEMINI_API_KEY is missing. The system remains testable in mock mode.",
                provider=self.name,
                model=self.model,
                raw={"error": "missing_gemini_api_key"},
            )
        try:
            from google import genai
            client = genai.Client(api_key=settings.gemini_api_key)
            resp = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
            text = getattr(resp, "text", None) or str(resp)
            return ProviderResult(answer=text, provider=self.name, model="gemini-1.5-flash", raw={})
        except Exception as exc:
            return ProviderResult(answer=f"Gemini generation failed: {exc}", provider=self.name, model=self.model, raw={"error": str(exc)})
