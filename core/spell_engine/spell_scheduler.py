class SpellScheduler:

    def compile(self, chain):

        graph = []

        for step in chain:
            graph.append({
                "agent": step["agent"],
                "task": step["task"],
                "status": "pending"
            })

        return graph