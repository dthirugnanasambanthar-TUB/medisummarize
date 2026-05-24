import json
from chunker import chunk_text
from embedder import embed_chunks
from store import store_chunks

def ingest_notes(notes_path: str):
    with open(notes_path) as f:
        notes = json.load(f)
    
    total_chunks = 0
    
    for note in notes:
        note_id = note["note_id"]
        raw_text = note["raw_text"]
        
        print(f"Processing {note_id}...", end=" ")
        
        chunks = chunk_text(raw_text)
        embeddings = embed_chunks(chunks)
        stored = store_chunks(note_id, chunks, embeddings)
        
        total_chunks += stored
        print(f"✓ {stored} chunks stored")
    
    print(f"\nDone. {total_chunks} total chunks stored for {len(notes)} notes.")

if __name__ == "__main__":
    ingest_notes("fixtures/patient_notes.json")