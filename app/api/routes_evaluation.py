from fastapi import APIRouter
from app.schemas import CompareRunsRequest, EvaluationRunRequest
from app.evaluation.evaluator import EvaluationRunner
from app.evaluation.regression import compare_runs

router = APIRouter(prefix="/evaluation", tags=["evaluation"])

@router.post("/run")
def run_evaluation(request: EvaluationRunRequest):
    return EvaluationRunner().run(provider=request.provider, top_k=request.top_k, prompt_version=request.prompt_version, limit=request.limit)

@router.post("/compare")
def compare(request: CompareRunsRequest):
    return compare_runs(request.run_a, request.run_b)
