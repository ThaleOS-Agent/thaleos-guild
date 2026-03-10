"""
agent_template.py
Base template for all ThaléOS agents.
"""

import json
import traceback


class AgentBase:
    def __init__(self, name, version="1.0", description="Generic Agent"):
        self.name = name
        self.version = version
        self.description = description

    def handle(self, payload: dict):
        """Override this method in your agent."""
        return {"status": "error", "message": "Not Implemented"}

    def execute(self, payload: dict):
        try:
            result = self.handle(payload)
            return json.dumps({"agent": self.name, "result": result})
        except Exception as e:
            return json.dumps({
                "agent": self.name,
                "error": str(e),
                "trace": traceback.format_exc()
            })
