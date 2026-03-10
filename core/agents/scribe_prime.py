from agents.agent_template import AgentBase

class ScribePrimeAgent(AgentBase):
    def __init__(self):
        super().__init__("scribe_prime", description="Advanced document generator and writer")

    def handle(self, payload):
        doc_type = payload.get("doc_type", "report")
        return {"status": "ok", "document": f"ScribePrime created {doc_type} successfully."}

agent = ScribePrimeAgent()
