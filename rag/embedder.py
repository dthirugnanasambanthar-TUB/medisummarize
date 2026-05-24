from sentence_transformers import SentenceTransformer
from typing import List

# Load once at module level — not inside the function
# This is important: loading the model takes ~2 seconds
# You don't want that happening on every single API request
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    embeddings = model.encode(chunks, convert_to_numpy=True)
    return embeddings.tolist()

if __name__ == "__main__":
    chunks = [
        "Patient is allergic to penicillin",
        "BP is 145/90, heart rate 100",
        "Plan to refer to cardiology"
    ]
    
    embeddings = embed_chunks(chunks)
    
    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Dimensions per embedding: {len(embeddings[0])}")
    print(f"First 5 values of embedding 1: {embeddings[0][:5]}")