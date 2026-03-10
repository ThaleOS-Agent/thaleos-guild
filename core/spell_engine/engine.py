from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .dsl import SpellDSL
from .memory import MemoryStore, FileMemoryStore
from .scheduler import TaskGraphScheduler, TaskNode
from .bus import EventBus
from .policies import PolicyGate
from .models import CastContext, CastResult

@dataclass
class Agent:
    name: str
    def run(self, action: str, payload: Dict[str, Any], ctx: CastContext) -> Dict[str, Any]:
        raise NotImplementedError

class SpellEngine:
    def __init__(
        self,
        agents: Dict[str, Agent],
        manifest_path: str,
        memory: Optional[MemoryStore] = None,
        bus: Optional[EventBus] = None,
        policy: Optional[PolicyGate] = None,
    ):
        self.agents = agents
        self.dsl = SpellDSL.from_yaml(manifest_path)
        self.memory = memory or FileMemoryStore("./.thaleos_memory.json")
        self.bus = bus or EventBus()
        self.policy = policy or PolicyGate()

        self.scheduler = TaskGraphScheduler(
            agents=self.agents,
            memory=self.memory,
            bus=self.bus,
            policy=self.policy,
        )

    def cast(self, user_text: str, session_id: str = "default", meta: Optional[dict]=None) -> CastResult:
        meta = meta or {}
        ctx = CastContext(session_id=session_id, user_text=user_text, meta=meta)

        spell = self.dsl.match(user_text)
        if not spell:
            return CastResult(ok=False, message="No spell recognized.", spell_id=None, outputs={})

        # memory-aware: enrich ctx
        ctx.memory_context = self.memory.get_context(session_id=session_id, keys=spell.memory_keys())

        # policy check
        self.policy.validate_spell(spell, ctx)

        # build task graph from chain
        nodes: List[TaskNode] = []
        for i, step in enumerate(spell.chain):
            nodes.append(TaskNode(
                id=f"{spell.id}:{i}:{step.step}",
                agent=step.agent,
                action=step.action,
                input=step.input or {},
                uses_memory=step.uses_memory or [],
                collaborate_with=step.collaborate_with or [],
                retries=step.retries,
                timeout_s=step.timeout_s,
                depends_on=[nodes[i-1].id] if i > 0 else [],
            ))

        outputs = self.scheduler.run(ctx=ctx, nodes=nodes)

        # write back outcomes
        self.memory.put_fact(session_id, "last_spell_id", spell.id)
        self.memory.put_fact(session_id, "last_spell_outcome", {"ok": True, "spell": spell.id})
        return CastResult(ok=True, message=f"Spell cast: {spell.name}", spell_id=spell.id, outputs=outputs)