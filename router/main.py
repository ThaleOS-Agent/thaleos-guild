import os
from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {
        "system": "ThaleOS Guild",
        "status": "online",
        "service": "orchestrator",
        "health_endpoint": "/health"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/system")
def system():
    return {
        "agents": ["UTILIX", "Guardian", "ChronaGate"],
        "environment": "render-cloud",
        "version": "0.3"
    }

# Alias to survive accidental probes/typos seen in your logs
@app.get("/heath")
def heath_alias():
    return {"ok": True, "service": "guild-console", "alias": "heath->health"}

@app.post("/activate")
def activate(agent: str):
    return {"agent": agent, "status": "activated"}

@app.post("/activate")
async def activate(req: Request):
    body = await req.json()
    spell = (body.get("spell") or "").strip()
    # Minimal: always respond; add auth later
    return {"ok": True, "spell": spell or "none", "received": True}