from app.agent.query_classifier import QueryClassifier

def test_contract_query_routes_to_rag():
    d = QueryClassifier().classify("What documents are required to change a contract?")
    assert d.route == "rag_answer"
    assert d.requires_retrieval is True

def test_weather_is_unsupported():
    d = QueryClassifier().classify("weather in Berlin")
    assert d.route == "unsupported_fallback"
