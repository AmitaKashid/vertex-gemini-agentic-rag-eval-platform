from functools import lru_cache
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.config import settings
from app.schemas import RetrievedChunk
from app.retrieval.chunker import MarkdownChunker

class Retriever:
    def __init__(self):
        self.index = _load_index()

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievedChunk]:
        chunks, vectorizer, matrix = self.index
        if not chunks:
            return []
        query_vec = vectorizer.transform([query])
        scores = cosine_similarity(query_vec, matrix).ravel()
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
        return [RetrievedChunk(document_id=chunks[i]["document_id"], chunk_id=chunks[i]["chunk_id"], score=float(score), text=chunks[i]["text"]) for i, score in ranked if score > 0]

@lru_cache(maxsize=1)
def _load_index():
    chunker = MarkdownChunker()
    docs_dir = Path(settings.document_dir)
    chunks = []
    for path in sorted(docs_dir.glob("*.md")):
        chunks.extend(chunker.chunk_file(path))
    texts = [c["text"] for c in chunks]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(texts) if texts else vectorizer.fit_transform(["empty"])
    return chunks, vectorizer, matrix
