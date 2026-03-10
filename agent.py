# agent.py
import asyncio
from event_bus import EventBus
from drives import DRIVES
from memory import Episodic, Procedural

class Agent:
    def __init__(self, name, bus, episodic, procedural):
        self.name=name; self.bus=bus; self.ep=episodic; self.proc=procedural

    async def observe(self, event): 
        # update memory, maybe spawn goals
        pass

    async def act(self):
        # 1) Intrinsic goals if idle
        for g in DRIVES.propose_goals():
            await self.bus.publish("goal", {"by": self.name, **g})

        # 2) Pick a goal from bus and plan (LLM/toolmix not shown)
        # 3) Execute skill(s), emit evaluation + memory_write
        # 4) If failure, propose skill_proposal (autopoiesis)

    async def loop(self):
        async for _, kind, payload in self.bus.stream("$"):
            if kind in ("observation","evaluation","memory_write"): 
                await self.observe((kind,payload))
            await self.act()

async def main():
    bus=EventBus("redis://localhost:6379"); await bus.start()
    agent=Agent("UTILIX", bus, Episodic("http://localhost:6333"), Procedural())
    await agent.loop()

if __name__=="__main__":
    asyncio.run(main())