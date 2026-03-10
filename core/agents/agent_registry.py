# core/agents/agent_registry.py
"""
Agent Registry - agent_registry.py

- Maintains a registry of agents with:
  - name, role, endpoint, health endpoint, metadata
- Provides:
  - register / unregister
  - list agents
  - ping health checks
- File-backed persistence (JSON) for dev/MVP.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="ThaleOS Agent Registry", version="0.1.0")

DATA_DIR = Path(os.environ.get("THALEOS_DATA_DIR", ".thaleos_data"))
REGISTRY_PATH = DATA_DIR / "agent_registry.json"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_registry() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {"agents": {}}
    try:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"agents": {}}


def _save_registry(reg: Dict[str, Any]) -> None:
    tmp = REGISTRY_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(REGISTRY_PATH)


class AgentInfo(BaseModel):
    name: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
    endpoint: str = Field(..., min_length=1, description="Base URL, e.g. http://localhost:9101")
    health_path: str = Field("/health", description="Health path appended to endpoint")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RegisterResponse(BaseModel):
    ok: bool
    agent: AgentInfo
    registered_at: float


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True, "service": "agent_registry", "ts": time.time()}


@app.post("/agents/register", response_model=RegisterResponse)
def register_agent(agent: AgentInfo) -> RegisterResponse:
    reg = _load_registry()
    reg["agents"][agent.name] = {
        "role": agent.role,
        "endpoint": agent.endpoint,
        "health_path": agent.health_path,
        "metadata": agent.metadata,
        "registered_at": time.time(),
    }
    _save_registry(reg)
    return RegisterResponse(ok=True, agent=agent, registered_at=reg["agents"][agent.name]["registered_at"])


@app.delete("/agents/{name}")
def unregister_agent(name: str) -> Dict[str, Any]:
    reg = _load_registry()
    if name not in reg["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    reg["agents"].pop(name)
    _save_registry(reg)
    return {"ok": True, "removed": name}


@app.get("/agents")
def list_agents() -> Dict[str, Any]:
    reg = _load_registry()
    return {"ok": True, "agents": reg["agents"]}


@app.get("/agents/{name}")
def get_agent(name: str) -> Dict[str, Any]:
    reg = _load_registry()
    if name not in reg["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"ok": True, "agent": {name: reg["agents"][name]}}


@app.post("/agents/{name}/ping")
async def ping_agent(name: str, timeout_s: int = 5) -> Dict[str, Any]:
    reg = _load_registry()
    if name not in reg["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")

    a = reg["agents"][name]
    url = a["endpoint"].rstrip("/") + "/" + a["health_path"].lstrip("/")

    try:
        async with httpx.AsyncClient(timeout=timeout_s) as client:
            r = await client.get(url)
        return {"ok": True, "name": name, "status_code": r.status_code, "health": r.json() if r.headers.get("content-type","").startswith("application/json") else r.text}
    except Exception as e:
        return {"ok": False, "name": name, "error": str(e)}