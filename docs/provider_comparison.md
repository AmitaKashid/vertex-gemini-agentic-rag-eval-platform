# Provider Comparison

The provider layer supports:

- `mock`: deterministic local provider for tests and offline demos.
- `local_http`: OpenAI-compatible local endpoint for llama.cpp, LM Studio, Ollama adapters, or custom inference servers.
- `gemini`: Gemini API provider when `GEMINI_API_KEY` is configured.

All providers receive the same prompt, context, and metadata. This enables fair comparison across quality, latency, and failure behavior.
