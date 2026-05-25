from pydantic import BaseModel
from typing import List

# Request models
class SummariseRequest(BaseModel):
    note_id: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

# Response models
class SOAPResponse(BaseModel):
    note_id: str
    subjective: str
    objective: str
    assessment: str
    plan: str

class SearchResult(BaseModel):
    note_id: str
    chunk_text: str
    similarity: float

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]