from __future__ import annotations
from typing import Any, Callable, Dict, List

class EventBus:
    def __init__(self):
        self._subs: Dict[str, List[Callable[[dict], None]]] = {}

    def subscribe(self, topic: str, fn: Callable[[dict], None]) -> None:
        self._subs.setdefault(topic, []).append(fn)

    def publish(self, topic: str, event: dict) -> None:
        for fn in self._subs.get(topic, []):
            fn(event)