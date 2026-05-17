install:
	pip install -e ".[dev]"

ingest:
	python scripts/ingest_documents.py

api:
	uvicorn app.main:app --reload

test:
	pytest -q

benchmark:
	python scripts/run_benchmark.py --provider mock --top-k 3 --prompt-version v1
