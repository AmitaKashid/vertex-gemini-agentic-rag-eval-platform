from app.retrieval.retriever import Retriever

if __name__ == "__main__":
    r = Retriever()
    chunks, _, _ = r.index
    print(f"Indexed {len(chunks)} document chunks.")
