from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from thaleos_api.config import settings
from thaleos_api.routes.health import router as health_router
from thaleos_api.routes.registry import router as registry_router
from thaleos_api.routes.orchestrator import router as orch_router
from thaleos_api.routes.utilix_proxy import router as utilix_router

app = FastAPI(title="ThaleOS Orchestrator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.thaleos_cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(registry_router)
app.include_router(orch_router)
app.include_router(utilix_router)

@app.get("/")
def root():
    return {"system": "ThaleOS Guild", "status": "online", "health": "/health"}