import argparse
from rich import print
from app.evaluation.regression import compare_runs

parser = argparse.ArgumentParser()
parser.add_argument("--run-a", required=True)
parser.add_argument("--run-b", required=True)
args = parser.parse_args()
print(compare_runs(args.run_a, args.run_b))
