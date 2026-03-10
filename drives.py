# drives.py
from dataclasses import dataclass, field
import random, time

@dataclass
class Drive:
    name: str
    weight: float
    measure: callable   # returns [0..1]
    target: float

class DriveManager:
    def __init__(self, drives): self.drives=drives
    def deficits(self):
        D=[]
        for d in self.drives:
            v=d.measure(); gap=max(0.0, d.target - v)
            D.append((d.name, d.weight*gap, v))
        return sorted(D, key=lambda x:-x[1])
    def propose_goals(self):
        goals=[]
        for name, score, val in self.deficits():
            if score<0.05: continue
            if name=="curiosity": goals.append({"kind":"explore_domain","hint":"unseen tool/API"})
            if name=="competence": goals.append({"kind":"improve_skill","hint":"retry failing tasks"})
            if name=="coherence": goals.append({"kind":"refactor_memory","hint":"merge duplicates + write summary"})
            if name=="safety": goals.append({"kind":"audit_action","hint":"dry-run dangerous ops"})
        return goals

# Example sensors (replace with real metrics)
def novelty_rate(): return random.uniform(0.0, 1.0)        # new embeddings vs known
def success_rate(): return 0.6                              # rolling task success
def memory_coherence(): return 0.5                          # deduped/linked %
def safety_score(): return 0.9                              # gatekeeper pass rate

DRIVES = DriveManager([
    Drive("curiosity",  0.25, novelty_rate,     0.6),
    Drive("competence", 0.35, success_rate,     0.8),
    Drive("coherence",  0.25, memory_coherence, 0.8),
    Drive("safety",     0.15, safety_score,     0.95),
])