# event_bus.py
import json, asyncio, aioredis
CHANNEL = "thaleos.events"

class EventBus:
    def __init__(self, url): self.url=url
    async def start(self): self.redis = await aioredis.from_url(self.url, decode_responses=True)
    async def publish(self, kind, payload): 
        await self.redis.xadd(CHANNEL, {"kind": kind, "data": json.dumps(payload)})
    async def stream(self, last_id="$"):
        while True:
            msgs = await self.redis.xread({CHANNEL: last_id}, block=5_000, count=50)
            if msgs:
                _, entries = msgs[0]
                for mid, fields in entries:
                    yield mid, fields["kind"], json.loads(fields["data"])
                last_id = entries[-1][0]