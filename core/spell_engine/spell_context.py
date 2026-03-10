class SpellContext:

    def __init__(self, spell_id, spell_name, intent):

        self.spell_id = spell_id
        self.spell_name = spell_name
        self.intent = intent

        self.memory = {}
        self.outputs = {}
        self.history = []

    def remember(self, key, value):
        self.memory[key] = value

    def recall(self, key):
        return self.memory.get(key)

    def log(self, event):
        self.history.append(event)