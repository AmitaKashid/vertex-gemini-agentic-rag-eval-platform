from app.retrieval.retriever import Retriever

def test_retriever_finds_contract_policy():
    chunks = Retriever().retrieve("contract change required documents", top_k=2)
    assert chunks
    assert any("contract" in c.document_id for c in chunks)
