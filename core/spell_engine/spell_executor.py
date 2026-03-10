class SpellExecutor:

    def __init__(self, guild, memory):

        self.guild = guild
        self.memory = memory

    async def execute(self, graph, context):

        results = []

        for node in graph:

            agent_name = node["agent"]
            task = node["task"]

            agent = self.guild.agents[agent_name]

            response = await agent.process_command(task)

            results.append(response)

            context.log({
                "agent": agent_name,
                "task": task,
                "result": response.content
            })

        return results