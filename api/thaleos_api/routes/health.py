from fastapi import APIRouter
from thaleos_api.models import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", service="orchestrator")