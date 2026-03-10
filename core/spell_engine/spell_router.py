import json
import pathlib

SPELL_FILE = pathlib.Path(__file__).parent / "spell_manifest.json"

class SpellRouter:

    def __init__(self):
        with open(SPELL_FILE) as f:
            self.manifest = json.load(f)["spells"]

    def resolve(self, text):

        text = text.lower()

        for spell in self.manifest:
            for phrase in spell["phrases"]:
                if phrase in text:
                    return {
                        "agent": spell["agent"],
                        "action": spell["action"],
                        "payload": {"input": text}
                    }

        return None