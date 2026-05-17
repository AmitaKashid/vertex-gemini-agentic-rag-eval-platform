import re
from app.schemas import RetrievedChunk

class EvidenceVerifier:
    def verify(self, answer: str, chunks: list[RetrievedChunk]) -> dict:
        if not chunks:
            return {"faithfulness": 0.0, "citation_coverage": 0.0, "hallucination_risk": 1.0, "supported": False}
        context = " ".join(c.text.lower() for c in chunks)
        sentences = [s.strip() for s in re.split(r"[.!?]+", answer) if s.strip()]
        if not sentences:
            return {"faithfulness": 0.0, "citation_coverage": 0.0, "hallucination_risk": 1.0, "supported": False}
        supported = 0
        for s in sentences:
            words = [w for w in re.findall(r"[a-zA-Z]{4,}", s.lower()) if w not in {"based", "should", "could", "would", "customer"}]
            if not words:
                continue
            overlap = sum(1 for w in words if w in context) / max(len(words), 1)
            if overlap >= 0.35:
                supported += 1
        faithfulness = supported / len(sentences)
        return {
            "faithfulness": round(faithfulness, 3),
            "citation_coverage": 1.0 if chunks else 0.0,
            "hallucination_risk": round(1 - faithfulness, 3),
            "supported": faithfulness >= 0.5,
        }
