from pathlib import Path
import pandas as pd

def export_summary_csv(run: dict, output_path: str | Path) -> None:
    rows = [{"metric": k, "value": v} for k, v in run.get("summary", {}).items()]
    pd.DataFrame(rows).to_csv(output_path, index=False)
