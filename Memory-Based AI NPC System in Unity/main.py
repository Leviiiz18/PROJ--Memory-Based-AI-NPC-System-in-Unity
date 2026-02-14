from fastapi import FastAPI
from pydantic import BaseModel
import os

# ===== MEMORY =====
from memory.short_memory import get_short_memory, add_to_short_memory
from memory.long_memory import load_memory, update_reputation

# ===== RAG =====
from rag.retriever import retrieve_lore, add_lore

# ===== PROMPT + LLM =====
from llm.prompt_builder import build_prompt
from llm.generator import generate_llm_response


app = FastAPI()


# ==========================================
# REQUEST / RESPONSE MODELS
# ==========================================

class ChatRequest(BaseModel):
    npc_name: str
    npc_type: str
    message: str


class ChatResponse(BaseModel):
    reply: str


# ==========================================
# LOAD LORE INTO VECTOR DB ON STARTUP
# ==========================================

@app.on_event("startup")
def load_lore():
    lore_path = "rag/lore/world_lore.txt"

    if os.path.exists(lore_path):
        with open(lore_path, "r", encoding="utf-8") as f:
            text = f.read()

        add_lore("world_lore", text)
        print("✅ Lore loaded into vector database.")
    else:
        print("⚠ No lore file found.")


# ==========================================
# CHAT ENDPOINT (UNITY CALLS THIS)
# ==========================================

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    # --------------------------------------
    # 1️⃣ LOAD MEMORY
    # --------------------------------------
    short_mem = get_short_memory(req.npc_name)
    player_data = load_memory()
    reputation = player_data.get("reputation", 0)

    # --------------------------------------
    # 2️⃣ UPDATE REPUTATION (SIMPLE LOGIC)
    # --------------------------------------
    msg_lower = req.message.lower()

    if "thank" in msg_lower or "thanks" in msg_lower:
        update_reputation(+1)

    if "idiot" in msg_lower or "stupid" in msg_lower:
        update_reputation(-2)

    # Reload updated reputation
    player_data = load_memory()
    reputation = player_data.get("reputation", 0)

    # --------------------------------------
    # 3️⃣ RETRIEVE LORE (RAG)
    # --------------------------------------
    lore_chunks = retrieve_lore(req.message)

    # --------------------------------------
    # 4️⃣ BUILD PROMPT
    # --------------------------------------
    prompt = build_prompt(
        npc_name=req.npc_name,
        npc_type=req.npc_type,
        short_memory=short_mem,
        lore_chunks=lore_chunks,
        reputation=reputation,
        user_message=req.message
    )

    # --------------------------------------
    # 5️⃣ GENERATE LLM RESPONSE
    # --------------------------------------
    reply = generate_llm_response(prompt)

    # Safety fallback
    if not reply:
        reply = "I have nothing to say right now."

    # --------------------------------------
    # 6️⃣ STORE SHORT MEMORY
    # --------------------------------------
    add_to_short_memory(req.npc_name, req.message, reply)

    # --------------------------------------
    # 7️⃣ RETURN TO UNITY
    # --------------------------------------
    return ChatResponse(reply=reply)