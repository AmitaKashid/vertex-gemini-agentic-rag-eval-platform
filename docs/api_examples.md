# API Examples

## Chat

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"What information is needed to schedule a callback?","provider":"mock","top_k":3}'
```

## Run Evaluation

```bash
curl -X POST http://localhost:8000/evaluation/run \
  -H "Content-Type: application/json" \
  -d '{"provider":"mock","top_k":3,"prompt_version":"v1"}'
```
