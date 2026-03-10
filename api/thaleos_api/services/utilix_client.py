import httpx
from thaleos_api.config import settings

class UtilixClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.utilix_base_url

    async def health(self) -> dict:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{self.base_url}/health")
            r.raise_for_status()
            return r.json()

    async def activate(self, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f"{self.base_url}/activate", json=payload)
            r.raise_for_status()
            return r.json()