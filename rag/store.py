import os
from supabase import create_client
from dotenv import load_dotenv
from typing import List

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def store_chunks(note_id: str, chunks: List[str], embeddings: List[List[float]]):
    rows = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        rows.append({
            "note_id": note_id,
            "chunk_index": i,
            "chunk_text": chunk,
            "embedding": embedding
        })
    
    result = supabase.table("document_chunks").insert(rows).execute()
    return len(result.data)