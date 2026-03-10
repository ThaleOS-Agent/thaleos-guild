import asyncio
from thaleos_utilix.api_client import OrchestratorAPI
from thaleos_utilix.config import settings

async def heartbeat_loop():
    api = OrchestratorAPI()
    endpoint = f"http://utilix:{settings.utilix_port}"  # container DNS name
    while True:
        try:
            await api.register(settings.utilix_id, endpoint)
        except Exception:
            # silent retry; keep daemon alive
            pass
        await asyncio.sleep(settings.utilix_heartbeat_seconds)