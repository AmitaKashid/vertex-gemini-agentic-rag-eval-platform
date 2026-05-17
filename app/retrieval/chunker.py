from pathlib import Path

class MarkdownChunker:
    def chunk_file(self, path: Path) -> list[dict]:
        text = path.read_text(encoding="utf-8")
        sections = [s.strip() for s in text.split("\n## ") if s.strip()]
        chunks = []
        for idx, sec in enumerate(sections):
            if idx > 0:
                sec = "## " + sec
            chunks.append({"document_id": path.name, "chunk_id": f"{path.stem}_{idx+1}", "text": sec})
        return chunks
