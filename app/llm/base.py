from abc import ABC, abstractmethod
from typing import Any
from app.schemas import ProviderResult

class LLMProvider(ABC):
    name: str
    model: str

    @abstractmethod
    def generate(self, prompt: str, context: list[str], metadata: dict[str, Any]) -> ProviderResult:
        raise NotImplementedError
