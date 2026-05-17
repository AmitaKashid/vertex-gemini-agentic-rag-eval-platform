import argparse
from app.observability.experiment_store import ExperimentStore
from app.evaluation.reports import export_summary_csv

parser = argparse.ArgumentParser()
parser.add_argument("--run-id", required=True)
parser.add_argument("--output", default="summary.csv")
args = parser.parse_args()
run = ExperimentStore().get_run(args.run_id)
if not run:
    raise SystemExit("Run not found")
export_summary_csv(run, args.output)
print(f"Wrote {args.output}")
