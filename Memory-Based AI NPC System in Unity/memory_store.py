import json
import os

MEMORY_FOLDER = "npc_memories"

if not os.path.exists(MEMORY_FOLDER):
    os.makedirs(MEMORY_FOLDER)

def get_memory_path(npc_name):
    return os.path.join(MEMORY_FOLDER, f"{npc_name}.json")

def load_memory(npc_name):
    path = get_memory_path(npc_name)

    if not os.path.exists(path):
        return {
            "reputation": 0,
            "conversations": []
        }

    with open(path, "r") as f:
        return json.load(f)

def save_memory(npc_name, data):
    path = get_memory_path(npc_name)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def add_conversation(npc_name, user_msg, npc_reply):
    data = load_memory(npc_name)

    data["conversations"].append({
        "user": user_msg,
        "npc": npc_reply
    })

    # keep last 15 interactions
    data["conversations"] = data["conversations"][-15:]

    save_memory(npc_name, data)

def update_reputation(npc_name, delta):
    data = load_memory(npc_name)
    data["reputation"] += delta
    save_memory(npc_name, data)