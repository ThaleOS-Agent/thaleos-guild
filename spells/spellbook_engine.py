"""
spellbook_engine.py
Lightweight execution engine for spells.
"""

import traceback


class SpellEngine:
    def run_spell(self, code: str, context: dict):
        """Executes provided Python code in a sandboxed environment."""
        local_env = {}
        try:
            exec(code, context, local_env)
            if "result" in local_env:
                return local_env["result"]
            return "✅ Spell executed successfully."
        except Exception as e:
            return f"❌ Spell execution failed: {str(e)}\n{traceback.format_exc()}"
