from fastapi import APIRouter, Depends, HTTPException
from thaleos_api.deps import get_utilix

router = APIRouter(prefix="/utilix", tags=["utilix"])

@router.get("/health")
async def utilix_health(utilix=Depends(get_utilix)):
    try:
        return await utilix.health()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))