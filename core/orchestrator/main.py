from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Command(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ThaleOS online"}

@app.post("/chat")
def chat(cmd: Command):
    return {
        "timestamp": datetime.utcnow(),
        "response": f"Thaelia received: {cmd.message}"
    }