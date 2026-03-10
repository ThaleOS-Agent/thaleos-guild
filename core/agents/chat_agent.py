from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

SPELL_ENGINE = os.getenv("THALEOS_SPELL_ENGINE_URL", "http://localhost:9105")

app = FastAPI(title="ThaleOS Chat Agent")

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"ok": True, "service": "chat_agent"}

@app.post("/chat")
def chat(req: ChatRequest):
    msg = req.message.lower()

    if "awaken" in msg:
        r = requests.post(
            f"{SPELL_ENGINE}/spell/cast/deploy_agent",
            json={}
        )
        return {"response": "Thaelia awakening sequence initiated", "spell": r.json()}

    if "status" in msg:
        r = requests.get("http://localhost:8081/system/status")
        return {"response": "System status", "data": r.json()}

    return {"response": "Thaelia received your message", "message": req.message}