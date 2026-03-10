from __future__ import annotations
from typing import Any, Dict, List, Optional
import json
import os
import time

class MemoryStore:
    def get_context(self, session_id: str, keys: List[str]) -> Dict[str, Any]:
        raise NotImplementedError
    def put_fact(self, session_id: str, key: str, value: Any) -> None:
        raise NotImplementedError

class FileMemoryStore(MemoryStore):
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump({"sessions": {}}, f)

    def _load(self) -> dict:
        with open(self.path, "r") as f:
            return json.load(f)

    def _save(self, data: dict) -> None:
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def get_context(self, session_id: str, keys: List[str]) -> Dict[str, Any]:
        data = self._load()
        sess = data["sessions"].get(session_id, {})
        return {k: sess.get(k) for k in keys if k in sess}

    def put_fact(self, session_id: str, key: str, value: Any) -> None:
        data = self._load()
        data["sessions"].setdefault(session_id, {})
        data["sessions"][session_id][key] = {"value": value, "ts": time.time()}
        self._save(data)