# main.py  (minimal "guild-console" FastAPI router for Render)
import os
from typing import Any, Dict, Optional

import httpx
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="guild-console", version="0.1.0")

ACTIONS_API_KEY = os.getenv("ACTIONS_API_KEY", "")
UPSTREAM_UTILIX_URL = os.getenv("UPSTREAM_UTILIX_URL", "").rstrip("/")  # e.g. https://utilix-bridge.thaleos.network

def require_env() -> None:
    if not ACTIONS_API_KEY:
        raise HTTPException(500, "Missing ACTIONS_API_KEY")
    if not UPSTREAM_UTILIX_URL:
        raise HTTPException(500, "Missing UPSTREAM_UTILIX_URL")

@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True, "service": "guild-console", "upstream": bool(UPSTREAM_UTILIX_URL)}

@app.post("/activate")
async def activate(body: Dict[str, Any], x_actions_key: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    require_env()
    # Optional: require callers to supply the key too (recommended).
    if x_actions_key != ACTIONS_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            f"{UPSTREAM_UTILIX_URL}/activate",
            json=body,
            headers={"x-actions-key": ACTIONS_API_KEY},
        )
        try:
            data = r.json()
        except Exception:
            data = {"raw": r.text}
        return {"ok": r.is_success, "status_code": r.status_code, "upstream": data}