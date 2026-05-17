import argparse
from rich import print
from app.evaluation.evaluator import EvaluationRunner

parser = argparse.ArgumentParser()
parser.add_argument("--provider", default="mock")
parser.add_argument("--top-k", type=int, default=3)
parser.add_argument("--prompt-version", default="v1")
parser.add_argument("--limit", type=int, default=None)
args = parser.parse_args()

result = EvaluationRunner().run(provider=args.provider, top_k=args.top_k, prompt_version=args.prompt_version, limit=args.limit)
print(result)
