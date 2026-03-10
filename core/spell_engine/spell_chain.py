class SpellChain:

    def __init__(self):
        self.steps = []

    def add(self, agent, task):
        self.steps.append({
            "agent": agent,
            "task": task
        })

    def __iter__(self):
        return iter(self.steps)