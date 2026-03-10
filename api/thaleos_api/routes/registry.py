from fastapi import APIRouter, Depends
from thaleos_api.models import AgentRecord, RegisterAgentRequest
from thaleos_api.deps import get_registry

router = APIRouter(prefix="/registry", tags=["registry"])

@router.post("/agents", response_model=AgentRecord)
def register_agent(req: RegisterAgentRequest, reg=Depends(get_registry)):
    return reg.upsert(req)

@router.get("/agents", response_model=list[AgentRecord])
def list_agents(reg=Depends(get_registry)):
    return reg.list()

@router.get("/agents/{agent_id}", response_model=AgentRecord)
def get_agent(agent_id: str, reg=Depends(get_registry)):
    rec = reg.get(agent_id)
    if not rec:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="agent not found")
    return rec