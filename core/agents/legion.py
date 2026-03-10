from agents.agent_template import AgentBase

class LegionAgent(AgentBase):
    def __init__(self):
        super().__init__("legion", description="Multi-agent orchestrator and coordinator")

    def handle(self, payload):
        return {
            "status": "ok",
            "message": "Legion coordinating tasks across agents.",
            "task": payload.get("task", "none")
        }

agent = LegionAgent()
