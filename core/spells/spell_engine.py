# core/spells/spell_engine.py
"""
Spell Engine - spell_engine.py

- Loads spell definitions from YAML files.
- Executes a spell as a chain of steps:
  - each step calls an agent endpoint with an action + params
- For MVP: sequential execution with simple retry/timeout.

Spell YAML example:
name: deploy_agent
description: Deploy a new agent
steps:
  - agent: utilix
    action: prepare_environment
    params: { ... }

Agent contract (HTTP):
POST {agent.endpoint}/action
{
  "action": "prepare_environment",
  "params": {...},
  "context": {...}
}
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="ThaleOS Spell Engine", version="0.1.0")

SPELLS_DIR = Path(os.environ.get("THALEOS_SPELLS_DIR", "spells")).resolve()
AGENT_REGISTRY_URL = os.environ.get("THALEOS_AGENT_REGISTRY_URL", "http://localhost:9100").rstrip("/")

DEFAULT_TIMEOUT = int(os.environ.get("THALEOS_SPELL_TIMEOUT_S", "20"))
DEFAULT_RETRIES = int(os.environ.get("THALEOS_SPELL_RETRIES", "1"))

START_TS = time.time()


class CastRequest(BaseModel):
    context: Dict[str, Any] = Field(default_factory=dict)
    dry_run: bool = False
    timeout_s: int = Field(DEFAULT_TIMEOUT, ge=1, le=300)
    retries: int = Field(DEFAULT_RETRIES, ge=0, le=5)


class StepResult(BaseModel):
    agent: str
    action: str
    ok: bool
    status_code: int
    response: Any


class CastResponse(BaseModel):
    ok: bool
    spell: str
    started_at: float
    finished_at: float
    results: List[StepResult]


def _load_spell(name: str) -> Dict[str, Any]:
    path = (SPELLS_DIR / f"{name}.yaml").resolve()
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Spell not found: {name}")
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid spell YAML: {e}")


async def _get_agent_endpoint(agent_name: str, timeout_s: int) -> str:
    url = f"{AGENT_REGISTRY_URL}/agents/{agent_name}"
    async with httpx.AsyncClient(timeout=timeout_s) as client:
        r = await client.get(url)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Agent registry lookup failed: {agent_name}")
    data = r.json()
    agent_block = data.get("agent", {}).get(agent_name)
    if not agent_block:
        raise HTTPException(status_code=404, detail=f"Agent not registered: {agent_name}")
    return agent_block["endpoint"]


async def _call_agent_action(endpoint: str, agent: str, action: str, params: Dict[str, Any], context: Dict[str, Any], timeout_s: int, retries: int) -> StepResult:
    url = endpoint.rstrip("/") + "/action"
    payload = {"action": action, "params": params or {}, "context": context or {}}

    last_err: Any = None
    for attempt in range(retries + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout_s) as client:
                r = await client.post(url, json=payload)
            ok = 200 <= r.status_code < 300
            resp: Any
            ct = r.headers.get("content-type", "")
            if ct.startswith("application/json"):
                resp = r.json()
            else:
                resp = r.text
            return StepResult(agent=agent, action=action, ok=ok, status_code=r.status_code, response=resp)
        except Exception as e:
            last_err = str(e)
            if attempt < retries:
                await httpx.AsyncClient().aclose()  # no-op safety
                time.sleep(0.2)
                continue

    return StepResult(agent=agent, action=action, ok=False, status_code=0, response={"error": last_err})


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "ok": True,
        "service": "spell_engine",
        "spells_dir": str(SPELLS_DIR),
        "agent_registry": AGENT_REGISTRY_URL,
        "uptime_s": round(time.time() - START_TS, 2),
        "ts": time.time(),
    }


@app.get("/spells")
def list_spells() -> Dict[str, Any]:
    if not SPELLS_DIR.exists():
        return {"ok": True, "spells": []}
    spells = sorted([p.stem for p in SPELLS_DIR.glob("*.yaml")])
    return {"ok": True, "spells": spells}


@app.post("/spell/cast/{spell_name}", response_model=CastResponse)
async def cast_spell(spell_name: str, req: CastRequest) -> CastResponse:
    spec = _load_spell(spell_name)
    steps = spec.get("steps", [])
    if not isinstance(steps, list) or not steps:
        raise HTTPException(status_code=400, detail="Spell has no steps")

    started = time.time()
    results: List[StepResult] = []

    # execute sequentially
    for s in steps:
        agent = s.get("agent")
        action = s.get("action")
        params = s.get("params", {}) or {}
        if not agent or not action:
            raise HTTPException(status_code=400, detail="Invalid step (missing agent/action)")

        endpoint = await _get_agent_endpoint(agent, timeout_s=req.timeout_s)

        if req.dry_run:
            results.append(StepResult(agent=agent, action=action, ok=True, status_code=200, response={"dry_run": True, "endpoint": endpoint, "params": params}))
            continue

        step_res = await _call_agent_action(
            endpoint=endpoint,
            agent=agent,
            action=action,
            params=params,
            context=req.context,
            timeout_s=req.timeout_s,
            retries=req.retries,
        )
        results.append(step_res)

        if not step_res.ok:
            finished = time.time()
            return CastResponse(ok=False, spell=spell_name, started_at=started, finished_at=finished, results=results)

    finished = time.time()
    return CastResponse(ok=True, spell=spell_name, started_at=started, finished_at=finished, results=results)