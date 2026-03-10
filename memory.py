# memory.py
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import time, hashlib

class Episodic:
    def __init__(self, url): 
        self.q = QdrantClient(url=url)
        try:
            self.q.create_collection("episodes", vectors_config=VectorParams(size=1536, distance=Distance.COSINE))
        except: pass
    def _id(self, text): return int(hashlib.md5(text.encode()).hexdigest()[:15], 16)
    def add(self, text, vec, meta):
        self.q.upsert("episodes", [PointStruct(id=self._id(f"{time.time()}-{text}"), vector=vec, payload={"text": text, **meta})])

class Procedural:
    def __init__(self): self.skills = {}  # name -> func, meta
    def register(self, name, func, meta): self.skills[name] = {"fn": func, "meta": meta}
    def list(self): return {k:v["meta"] for k,v in self.skills.items()}