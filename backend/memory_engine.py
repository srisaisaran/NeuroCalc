import json
import os


class MemoryEngine:

    def __init__(self):

        self.file = "memory.json"

        self.memory = self.load_memory()


    def load_memory(self):

        if os.path.exists(self.file):

            with open(self.file, "r") as f:
                return json.load(f)

        return {}


    def save_memory(self):

        with open(self.file, "w") as f:
            json.dump(
                self.memory,
                f,
                indent=4
            )


    def remember(self, key, value):

        self.memory[key] = value

        self.save_memory()


    def recall(self, key):

        return self.memory.get(key, None)