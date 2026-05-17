from abc import ABC, abstractmethod
from app.schemas import RetrievedChunk

class VectorStore(ABC):
    @abstractmethod
    def retrieve(self, query: str, top_k: int) -> list[RetrievedChunk]:
        raise NotImplementedError
