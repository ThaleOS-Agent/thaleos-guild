"""
integration_template.py
Provides helper methods for integrating agents with the orchestrator.
"""

from agents.agent_template import AgentBase

class IntegrationAgent(AgentBase):
    def __init__(self, name, external_api):
        super().__init__(name, description=f"Integration agent for {external_api}")
        self.external_api = external_api

    def handle(self, payload):
        # Example integration logic
        return {
            "status": "success",
            "api": self.external_api,
            "data": payload,
            "note": "Integration endpoint reached successfully."
        }
