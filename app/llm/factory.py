from app.llm.mock_provider import MockProvider
from app.llm.local_http_provider import LocalHttpProvider
from app.llm.gemini_provider import GeminiProvider

PROVIDERS = {
    "mock": MockProvider,
    "local_http": LocalHttpProvider,
    "gemini": GeminiProvider,
}

def get_provider(name: str):
    provider_cls = PROVIDERS.get(name, MockProvider)
    return provider_cls()
