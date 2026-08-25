from memory_engine import MemoryEngine


memory = MemoryEngine()


memory.remember(
    "name",
    "Sai"
)


print(
    memory.recall("name")
)