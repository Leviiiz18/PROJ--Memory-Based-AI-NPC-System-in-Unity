import chromadb
from rag.embedder import embed_text

# Persistent DB (auto persistence in new versions)
client = chromadb.Client(
    settings=chromadb.Settings(
        persist_directory="vector_db",
        is_persistent=True
    )
)

collection = client.get_or_create_collection("lore")


# -------- Chunking --------
def chunk_text(text, chunk_size=400):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size].strip()
        if chunk:
            chunks.append(chunk)
    return chunks


# -------- Add Lore --------
def add_lore(id_prefix, full_text):

    chunks = chunk_text(full_text)

    existing_ids = collection.get()["ids"]

    for i, chunk in enumerate(chunks):

        chunk_id = f"{id_prefix}_{i}"

        if chunk_id in existing_ids:
            continue  # avoid duplicates

        collection.add(
            documents=[chunk],
            embeddings=[embed_text(chunk)],
            ids=[chunk_id]
        )


# -------- Retrieve Lore --------
def retrieve_lore(query, top_k=3):

    try:
        results = collection.query(
            query_embeddings=[embed_text(query)],
            n_results=top_k
        )

        if results and results["documents"]:
            return results["documents"][0]

    except Exception as e:
        print("RAG Retrieval Error:", e)

    return []