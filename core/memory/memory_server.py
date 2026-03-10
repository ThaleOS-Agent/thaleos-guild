# core/memory/memory_server.py
"""
ThaleOS Memory Core - memory_server.py

- Lightweight FastAPI service for:
  - key/value "state" memory
  - append-only "events" log
  - simple vector store stub (pluggable)
- File-backed persistence (JSON) for dev/MVP.
"""

from __future__ import annotations

import json
import os
import threading
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# -----------------------------
# Persistence
# -----------------------------

DATA_DIR = Path(os.environ.get("THALEOS_DATA_DIR", ".thaleos_data"))
STATE_PATH = DATA_DIR / "memory_state.json"
EVENTS_PATH = DATA_DIR / "memory_events.jsonl"

DATA_DIR.mkdir(parents=True, exist_ok=True)


_lock = threading.Lock()


def _read_state() -> Dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_state(state: Dict[str, Any]) -> None:
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE_PATH)


def _append_event(evt: Dict[str, Any]) -> None:
    line = json.dumps(evt, ensure_ascii=False)
    with EVENTS_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


# -----------------------------
# Vector store (stub)
# -----------------------------

@dataclass
class VectorRecord:
    id: str
    text: str
    metadata: Dict[str, Any]
    created_at: float


class InMemoryVectorStore:
    """
    Minimal placeholder: stores text records and returns naive keyword matches.
    Swap this with FAISS/Chroma/pgvector later.
    """
    def __init__(self) -> None:
        self._items: List[VectorRecord] = []

    def add(self, rec: VectorRecord) -> None:
        self._items.append(rec)

    def search(self, query: str, k: int = 5) -> List[VectorRecord]:
        q = query.lower().strip()
        if not q:
            return []
        scored: List[tuple[int, VectorRecord]] = []
        for it in self._items:
            score = it.text.lower().count(q)
            if score > 0:
                scored.append((score, it))
        scored.sort(key=lambda t: t[0], reverse=True)
        return [r for _, r in scored[:k]]


VECTOR_STORE = InMemoryVectorStore()


# -----------------------------
# API Models
# -----------------------------

class PutStateRequest(BaseModel):
    key: str = Field(..., min_length=1)
    value: Any


class GetStateResponse(BaseModel):
    key: str
    value: Any


class AppendEventRequest(BaseModel):
    type: str = Field(..., min_length=1)
    payload: Dict[str, Any] = Field(default_factory=dict)


class AddVectorRequest(BaseModel):
    id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VectorSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    k: int = Field(5, ge=1, le=50)


class VectorSearchResult(BaseModel):
    id: str
    text: str
    metadata: Dict[str, Any]
    created_at: float


# -----------------------------
# FastAPI
# -----------------------------

app = FastAPI(title="ThaleOS Memory Core", version="0.1.0")


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "ok": True,
        "service": "memory_core",
        "state_path": str(STATE_PATH),
        "events_path": str(EVENTS_PATH),
        "vectors": len(VECTOR_STORE._items),
        "ts": time.time(),
    }


@app.put("/state", response_model=GetStateResponse)
def put_state(req: PutStateRequest) -> GetStateResponse:
    with _lock:
        state = _read_state()
        state[req.key] = req.value
        _write_state(state)
        _append_event({"type": "state.put", "key": req.key, "ts": time.time()})
    return GetStateResponse(key=req.key, value=req.value)


@app.get("/state/{key}", response_model=GetStateResponse)
def get_state(key: str) -> GetStateResponse:
    with _lock:
        state = _read_state()
    if key not in state:
        raise HTTPException(status_code=404, detail="Key not found")
    return GetStateResponse(key=key, value=state[key])


@app.post("/events")
def append_event(req: AppendEventRequest) -> Dict[str, Any]:
    evt = {"type": req.type, "payload": req.payload, "ts": time.time()}
    with _lock:
        _append_event(evt)
    return {"ok": True, "event": evt}


@app.post("/vectors/add")
def add_vector(req: AddVectorRequest) -> Dict[str, Any]:
    rec = VectorRecord(
        id=req.id,
        text=req.text,
        metadata=req.metadata,
        created_at=time.time(),
    )
    VECTOR_STORE.add(rec)
    with _lock:
        _append_event({"type": "vector.add", "id": req.id, "ts": time.time()})
    return {"ok": True, "stored": asdict(rec)}


@app.post("/vectors/search", response_model=List[VectorSearchResult])
def search_vectors(req: VectorSearchRequest) -> List[VectorSearchResult]:
    items = VECTOR_STORE.search(req.query, k=req.k)
    return [VectorSearchResult(**asdict(it)) for it in items]

from pydantic import BaseModel, Field
from typing import Any, Dict

class ActionRequest(BaseModel):
    action: str = Field(..., min_length=1)
    params: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)

@app.post("/action")
def action(req: ActionRequest) -> Dict[str, Any]:
    if req.action == "remember":
        key = str(req.params.get("key", "")).strip()
        if not key:
            raise HTTPException(status_code=400, detail="missing key")
        value = req.params.get("value")
        # reuse existing put_state logic
        put_state(PutStateRequest(key=key, value=value))
        return {"ok": True, "action": "remember", "key": key}
    raise HTTPException(status_code=404, detail=f"Unknown action: {req.action}")