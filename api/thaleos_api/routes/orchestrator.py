from fastapi import APIRouter, Depends, HTTPException
from thaleos_api.models import ActivationRequest, ActivationResponse
from thaleos_api.deps import get_orchestrator

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])

@router.post("/activate", response_model=ActivationResponse)
async def activate(req: ActivationRequest, orch=Depends(get_orchestrator)):
    try:
        result = await orch.activate_agent(req.agent_id, req.model_dump())
        return ActivationResponse(
            accepted=True,
            agent_id=req.agent_id,
            message="activation sent",
            result=result,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"agent call failed: {e}")