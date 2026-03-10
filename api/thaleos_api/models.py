from pydantic import BaseModel, Field
from typing import Literal, Any

class HealthResponse(BaseModel):
    status: Literal["ok"]
    system: str = "ThaleOS"
    service: str

class AgentRecord(BaseModel):
    agent_id: str
    kind: str = "agent"
    endpoint: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)
    last_seen_unix: float

class RegisterAgentRequest(BaseModel):
    agent_id: str
    endpoint: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)

class ActivationRequest(BaseModel):
    agent_id: str
    command: str = "activate"
    payload: dict[str, Any] = Field(default_factory=dict)

class ActivationResponse(BaseModel):
    accepted: bool
    agent_id: str
    message: str
    result: dict[str, Any] = Field(default_factory=dict)