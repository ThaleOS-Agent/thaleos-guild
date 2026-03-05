import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ThaleOS Guild API", version="0.1.0")

ENV = os.getenv("ENV", "local")
ACTIONS_API_KEY = os.getenv("ACTIONS_API_KEY", "dev-actions-key")
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]

if CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def require_key(x_actions_key: str | None):
    if not x_actions_key or x_actions_key != ACTIONS_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/health")
def health():
    return {"ok": True, "env": ENV}

@app.post("/activate")
def activate(payload: dict, x_actions_key: str | None = Header(default=None)):
    """
    Minimal activation endpoint used by Router / Desktop.
    Keep this thin; real orchestration can be wired later.
    """
    require_key(x_actions_key)
    spell = payload.get("spell") or payload.get("message") or ""
    return {
        "ok": True,
        "env": ENV,
        "received": payload,
        "note": "Activation accepted (placeholder). Wire real agents here."
    }

@app.get("/.well-known/openapi.json")
def openapi_alias():
    return app.openapi()
