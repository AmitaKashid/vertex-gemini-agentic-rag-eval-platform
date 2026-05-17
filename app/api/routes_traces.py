from fastapi import APIRouter, HTTPException
from app.observability.trace_logger import TraceLogger

router = APIRouter(prefix="/traces", tags=["traces"])
logger = TraceLogger()

@router.get("/{conversation_id}")
def get_trace(conversation_id: str):
    trace = logger.get_trace(conversation_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found")
    return trace
