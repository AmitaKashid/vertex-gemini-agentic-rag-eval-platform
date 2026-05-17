from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse
from app.agent.graph import AgentGraph

router = APIRouter(tags=["chat"])
agent = AgentGraph()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return agent.run(request)
