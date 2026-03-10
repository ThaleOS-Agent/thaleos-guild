from thaleos_api.services.registry_store import RegistryStore
from thaleos_api.services.utilix_client import UtilixClient

class OrchestratorCore:
    def __init__(self, registry: RegistryStore, utilix: UtilixClient):
        self.registry = registry
        self.utilix = utilix

    async def activate_agent(self, agent_id: str, payload: dict) -> dict:
        # For now: only UTILIX is action-capable by default.
        if agent_id.lower().startswith("utilix"):
            return await self.utilix.activate(payload)
        raise ValueError(f"Unknown or unsupported agent_id: {agent_id}")