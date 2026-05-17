from fastapi import APIRouter, HTTPException
from app.observability.experiment_store import ExperimentStore

router = APIRouter(prefix="/experiments", tags=["experiments"])
store = ExperimentStore()

@router.get("")
def list_experiments():
    return store.list_runs()

@router.get("/{run_id}")
def get_experiment(run_id: str):
    result = store.get_run(run_id)
    if not result:
        raise HTTPException(status_code=404, detail="Run not found")
    return result
