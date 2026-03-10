from agents.agent_template import AgentBase

class PulseAgent(AgentBase):
    def __init__(self):
        super().__init__("pulse", description="System health monitoring and heartbeat agent")

    def handle(self, payload):
        return {
            "status": "ok",
            "heartbeat": "Pulse active",
            "metrics": {"cpu": "normal", "memory": "optimal"}
        }

agent = PulseAgent()
