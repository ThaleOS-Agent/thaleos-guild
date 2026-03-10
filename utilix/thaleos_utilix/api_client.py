import httpx
from thaleos_utilix.config import settings

class OrchestratorAPI:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.thaleos_api_url

    async def register(self, agent_id: str, endpoint: str):
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.post(
                f"{self.base_url}/registry/agents",
                json={"agent_id": agent_id, "endpoint": endpoint, "meta": {"kind": "utilix"}},
            )
            r.raise_for_status()
            return r.json()