from functools import lru_cache
from thaleos_api.config import settings
from thaleos_api.services.registry_store import RegistryStore
from thaleos_api.services.utilix_client import UtilixClient
from thaleos_api.services.orchestrator_core import OrchestratorCore

@lru_cache
def get_registry() -> RegistryStore:
    return RegistryStore(ttl_seconds=settings.thaleos_registry_ttl_seconds)

@lru_cache
def get_utilix() -> UtilixClient:
    return UtilixClient()

@lru_cache
def get_orchestrator() -> OrchestratorCore:
    return OrchestratorCore(get_registry(), get_utilix())