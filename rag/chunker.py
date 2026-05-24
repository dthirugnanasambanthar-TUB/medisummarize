from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str, chunk_size: int = 200, chunk_overlap: int = 40) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_text(text)

if __name__ == "__main__":
    sample = """Patient is a 45-year-old female presenting with severe headache. 
She takes ibuprofen 400mg b.i.d. for chronic pain. BP is 130/85, HR 78.
Assessment suggests tension headache vs. migraine. Plan to start sumatriptan."""

    chunks = chunk_text(sample)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {chunk}")
        print("---")