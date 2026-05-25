from store import supabase
from embedder import embed_chunks


def search(question: str, top_k: int = 10) -> list[dict]:
    query_embeddings = embed_chunks([question])[0]
    try:
        result = supabase.rpc(
            "search_chunks",
            {
                "query_embedding": query_embeddings,
                "match_count": top_k
            }
        ).execute()
        return result.data
    
    except Exception as e:
        print(f"Search failed: {e}")
        return []

if __name__ == "__main__":
    results = search("does any patient have a penicillin allergy?")
    
    for r in results:
        print(f"Note: {r['note_id']} | Similarity: {r['similarity']:.3f}")
        print(f"Chunk: {r['chunk_text'][:100]}...")
        print("---")
        
    
    