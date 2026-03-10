import time
from typing import Dict
from thaleos_api.models import AgentRecord, RegisterAgentRequest

class RegistryStore:
    def __init__(self, ttl_seconds: int = 60):
        self.ttl_seconds = ttl_seconds
        self._agents: Dict[str, AgentRecord] = {}

    def upsert(self, req: RegisterAgentRequest) -> AgentRecord:
        now = time.time()
        rec = AgentRecord(
            agent_id=req.agent_id,
            endpoint=req.endpoint,
            meta=req.meta,
            last_seen_unix=now,
        )
        self._agents[req.agent_id] = rec
        return rec

    def touch(self, agent_id: str) -> AgentRecord | None:
        rec = self._agents.get(agent_id)
        if not rec:
            return None
        rec.last_seen_unix = time.time()
        self._agents[agent_id] = rec
        return rec

    def list(self) -> list[AgentRecord]:
        self._gc()
        return sorted(self._agents.values(), key=lambda r: r.agent_id)

    def get(self, agent_id: str) -> AgentRecord | None:
        self._gc()
        return self._agents.get(agent_id)

    def _gc(self) -> None:
        now = time.time()
        expired = [
            k for k, v in self._agents.items()
            if (now - v.last_seen_unix) > self.ttl_seconds
        ]
        for k in expired:
            self._agents.pop(k, None)