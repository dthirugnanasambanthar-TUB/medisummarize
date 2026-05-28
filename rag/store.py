import os
from supabase import create_client
from dotenv import load_dotenv
from typing import List,Optional

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

def get_chunks_by_note_id(note_id: str) -> list[str]:
    result = supabase.table("document_chunks") \
        .select("chunk_text") \
        .eq("note_id", note_id) \
        .order("chunk_index") \
        .execute()
    
    return [row["chunk_text"] for row in result.data]

def get_cached_summary(note_id: str) -> Optional[dict]:
    result = supabase.table("summaries") \
        .select("*") \
        .eq("note_id", note_id) \
        .execute()
    
    if result.data:
        return result.data[0]
    return None

def cache_summary(note_id: str, summary: dict) -> None:
    supabase.table("summaries").insert({
        "note_id": note_id,
        **summary
    }).execute()

if __name__ == "__main__":
    chunks = get_chunks_by_note_id("note_001")
    print(f"Found {len(chunks)} chunks for note_001")
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i}: {chunk[:60]}...")