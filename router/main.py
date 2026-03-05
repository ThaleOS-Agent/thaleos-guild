import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"ok": True, "service": "guild-console"}

@app.get("/health")
def health():
    return {"ok": True, "service": "guild-console"}

# Alias to survive accidental probes/typos seen in your logs
@app.get("/heath")
def heath_alias():
    return {"ok": True, "service": "guild-console", "alias": "heath->health"}

@app.post("/activate")
async def activate(req: Request):
    body = await req.json()
    spell = (body.get("spell") or "").strip()
    # Minimal: always respond; add auth later
    return {"ok": True, "spell": spell or "none", "received": True}