from __future__ import annotations

class PolicyGate:
    # v1: minimal safe defaults; expand as needed
    ALLOWED_AGENTS = {"utilix", "guardian", "scribe", "sagequery"}
    ALLOWED_ACTIONS = {
        "utilix": {"health", "sync", "snapshot"},
        "guardian": {"ensure_registry", "scan_system", "fetch_context", "compliance_check"},
        "scribe": {"write_log", "generate_report", "compose"},
        "sagequery": {"brief_status", "summarize_risks", "research"},
    }

    def validate_spell(self, spell, ctx):
        # placeholder: can enforce “modes” from memory here
        return True

    def validate_task(self, node, ctx):
        if node.agent not in self.ALLOWED_AGENTS:
            raise ValueError(f"Agent not allowed: {node.agent}")
        if node.action not in self.ALLOWED_ACTIONS.get(node.agent, set()):
            raise ValueError(f"Action not allowed: {node.agent}.{node.action}")
        return True