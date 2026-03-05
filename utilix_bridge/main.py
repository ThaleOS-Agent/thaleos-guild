import os
from typing import Optional, Dict, Any

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="UTILIX Agent Bridge", version="0.1.0")

ENV = os.getenv("ENV", "local")
ACTIONS_API_KEY = os.getenv("ACTIONS_API_KEY", "dev-actions-key")
UPSTREAM_UTILIX_URL = (os.getenv("UPSTREAM_UTILIX_URL", "http://127.0.0.1:8090")).rstrip("/")
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]

if CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def require_key(x_actions_key: Optional[str]) -> None:
    if not x_actions_key or x_actions_key != ACTIONS_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/health")
def health():
    return {"ok": True, "env": ENV, "upstream": UPSTREAM_UTILIX_URL}

@app.post("/activate")
async def activate(payload: Dict[str, Any], x_actions_key: Optional[str] = Header(default=None)):
    require_key(x_actions_key)
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            r = await client.post(
                f"{UPSTREAM_UTILIX_URL}/activate",
                json=payload,
                headers={"x-actions-key": ACTIONS_API_KEY},
            )
            try:
                data = r.json()
            except Exception:
                data = {"raw": r.text}
            return {"ok": r.is_success, "status_code": r.status_code, "upstream_body": data}
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Upstream error: {e}") from e
