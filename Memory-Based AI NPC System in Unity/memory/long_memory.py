import json
import os

MEMORY_PATH = "memory/player_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {"reputation": 0, "name": None}

    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_PATH, "w") as f:
        json.dump(data, f)

def update_reputation(delta):
    data = load_memory()
    data["reputation"] += delta
    save_memory(data)