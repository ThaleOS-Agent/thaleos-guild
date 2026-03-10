from agents.agent_template import AgentBase

class AurumAgent(AgentBase):
    def __init__(self):
        super().__init__("aurum", description="Handles financial and asset intelligence")

    def handle(self, payload):
        query = payload.get("query", "No query provided")
        return {"status": "ok", "insight": f"Aurum processed financial query: {query}"}

agent = AurumAgent()
