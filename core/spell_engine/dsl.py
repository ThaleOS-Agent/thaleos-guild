from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import yaml

@dataclass
class SpellStep:
    step: str
    agent: str
    action: str
    input: Optional[dict] = None
    uses_memory: Optional[list] = None
    collaborate_with: Optional[list] = None
    retries: int = 1
    timeout_s: int = 30

@dataclass
class Spell:
    id: str
    name: str
    triggers: List[str]
    intent: str
    chain: List[SpellStep]

    def memory_keys(self) -> List[str]:
        keys = set()
        for s in self.chain:
            for k in (s.uses_memory or []):
                keys.add(k)
        return list(keys)

class SpellDSL:
    def __init__(self, spells: List[Spell]):
        self.spells = spells

    @classmethod
    def from_yaml(cls, path: str) -> "SpellDSL":
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        spells = []
        for s in data["spells"]:
            chain = [SpellStep(**c) for c in s["chain"]]
            spells.append(Spell(
                id=s["id"],
                name=s["name"],
                triggers=[t.lower() for t in s["triggers"]],
                intent=s["intent"],
                chain=chain,
            ))
        return cls(spells)

    def match(self, user_text: str) -> Optional[Spell]:
        txt = user_text.lower()
        for s in self.spells:
            if any(t in txt for t in s.triggers):
                return s
        return None