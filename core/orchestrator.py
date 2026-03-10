import sys
import json

from spell_router import SpellRouter
from agents.guardian_agent import GuardianAgent
from agents.scribe_agent import ScribeAgent
from agents.sagequery_agent import SageQueryAgent
from agents.utilix_agent import UtilixAgent

router = SpellRouter()

agents = {
    "guardian": GuardianAgent(),
    "scribe": ScribeAgent(),
    "sagequery": SageQueryAgent(),
    "utilix": UtilixAgent()
}

def invoke_spell(text):

    spell = router.resolve(text)

    if not spell:
        return "No spell recognized."

    agent = agents.get(spell["agent"])

    if not agent:
        return "Agent not found."

    return agent.run(spell["action"], spell["payload"])


if __name__ == "__main__":

    agent_name = sys.argv[1]
    payload = json.loads(sys.argv[2])

    if "query" in payload:
        result = invoke_spell(payload["query"])
    else:
        result = agents[agent_name].run(payload["action"], payload)

    print(result)