from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time

from .models import CastContext
from .memory import MemoryStore
from .bus import EventBus
from .policies import PolicyGate

@dataclass
class TaskNode:
    id: str
    agent: str
    action: str
    input: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    uses_memory: List[str] = field(default_factory=list)
    collaborate_with: List[Dict[str, str]] = field(default_factory=list)
    retries: int = 1
    timeout_s: int = 30

class TaskGraphScheduler:
    def __init__(self, agents, memory: MemoryStore, bus: EventBus, policy: PolicyGate):
        self.agents = agents
        self.memory = memory
        self.bus = bus
        self.policy = policy

    def run(self, ctx: CastContext, nodes: List[TaskNode]) -> Dict[str, Any]:
        outputs: Dict[str, Any] = {}
        done = set()

        node_map = {n.id: n for n in nodes}

        def ready(n: TaskNode) -> bool:
            return all(d in done for d in n.depends_on)

        while len(done) < len(nodes):
            progressed = False
            for n in nodes:
                if n.id in done:
                    continue
                if not ready(n):
                    continue

                progressed = True
                outputs[n.id] = self._run_node(ctx, n, outputs)
                done.add(n.id)

            if not progressed:
                raise RuntimeError("Deadlock in task graph (check depends_on).")

        return outputs

    def _run_node(self, ctx: CastContext, node: TaskNode, outputs: Dict[str, Any]) -> Dict[str, Any]:
        self.policy.validate_task(node, ctx)

        agent = self.agents.get(node.agent)
        if not agent:
            raise RuntimeError(f"Agent not found: {node.agent}")

        payload = dict(node.input)

        # memory-aware injection
        if node.uses_memory:
            payload["memory"] = self.memory.get_context(ctx.session_id, node.uses_memory)

        # chain context + prior outputs
        payload["chain"] = {"user_text": ctx.user_text, "meta": ctx.meta, "prev": outputs}

        # collaboration pre-brief
        self.bus.publish("task.start", {"task_id": node.id, "agent": node.agent, "action": node.action})

        attempts = 0
        last_err = None
        while attempts <= node.retries:
            attempts += 1
            try:
                start = time.time()
                result = agent.run(node.action, payload, ctx)
                elapsed = time.time() - start

                # collaboration: request contributions
                if node.collaborate_with:
                    collab = self._collaborate(ctx, node, result)
                    result["collaboration"] = collab

                self.bus.publish("task.done", {"task_id": node.id, "elapsed_s": elapsed})
                return result

            except Exception as e:
                last_err = str(e)
                self.bus.publish("task.error", {"task_id": node.id, "error": last_err, "attempt": attempts})

        raise RuntimeError(f"Task failed after retries: {node.id} :: {last_err}")

    def _collaborate(self, ctx: CastContext, node: TaskNode, primary_result: Dict[str, Any]) -> Dict[str, Any]:
        contributions = {}
        for req in node.collaborate_with:
            agent_name = req["agent"]
            action = req["action"]
            agent = self.agents.get(agent_name)
            if not agent:
                continue
            payload = {
                "primary_task_id": node.id,
                "primary_result": primary_result,
                "memory": self.memory.get_context(ctx.session_id, ["preferred_modes", "project_context"]),
            }
            contributions[f"{agent_name}.{action}"] = agent.run(action, payload, ctx)
        return contributions