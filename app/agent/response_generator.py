from app.schemas import RetrievedChunk, RoutingDecision, ProviderResult
from app.llm.factory import get_provider

class ResponseGenerator:
    def generate(self, query: str, route: RoutingDecision, chunks: list[RetrievedChunk], provider_name: str, prompt_version: str) -> ProviderResult:
        if route.route == "clarification_needed":
            return ProviderResult(answer="Could you clarify your question and specify which policy or process you mean?", provider="system", model="guardrail")
        if route.route == "unsupported_fallback":
            return ProviderResult(answer="I cannot answer that from the available enterprise knowledge base. Please ask a question related to contracts, invoices, callbacks, verification, or escalation policies.", provider="system", model="guardrail")
        if route.route == "high_risk_fallback":
            return ProviderResult(answer="I cannot provide an unsupported or high-risk guarantee. I can only answer using retrieved policy evidence and will escalate uncertain cases.", provider="system", model="guardrail")
        provider = get_provider(provider_name)
        prompt = self._build_prompt(query, route, chunks, prompt_version)
        return provider.generate(prompt=prompt, context=[c.text for c in chunks], metadata={"route": route.route, "prompt_version": prompt_version})

    def _build_prompt(self, query: str, route: RoutingDecision, chunks: list[RetrievedChunk], prompt_version: str) -> str:
        evidence = "\n\n".join(f"[{i+1}] {c.text}" for i, c in enumerate(chunks))
        if prompt_version == "v2":
            return f"""You are an enterprise RAG assistant. Answer only using evidence. If evidence is insufficient, say so.\nRoute: {route.route}\nQuestion: {query}\nEvidence:\n{evidence}\nAnswer with concise bullet points and cite evidence numbers."""
        return f"""Answer the user question using the retrieved context. Do not invent details.\nQuestion: {query}\nContext:\n{evidence}\nAnswer:"""
