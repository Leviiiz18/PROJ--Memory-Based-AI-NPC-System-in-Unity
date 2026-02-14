conversation_memory = {}

def get_short_memory(npc_name):
    return conversation_memory.get(npc_name, [])

def add_to_short_memory(npc_name, user_msg, npc_reply):
    if npc_name not in conversation_memory:
        conversation_memory[npc_name] = []

    conversation_memory[npc_name].append({
        "user": user_msg,
        "npc": npc_reply
    })

    # Keep only last 6 exchanges
    conversation_memory[npc_name] = conversation_memory[npc_name][-6:]