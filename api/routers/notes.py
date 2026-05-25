import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../rag'))

from fastapi import APIRouter, HTTPException
from api.schema import (
    SummariseRequest, SOAPResponse,
    SearchRequest, SearchResponse, SearchResult
)
from rag.summariser import summarise_note
from rag.retriever import search

router = APIRouter(prefix="/api/v1", tags=["notes"])

@router.post("/summarise", response_model=SOAPResponse)
async def summarise(request: SummariseRequest):
    try:
        summary = summarise_note(request.note_id)
        return SOAPResponse(
            note_id=request.note_id,
            **summary.model_dump()
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=SearchResponse)
async def search_notes(request: SearchRequest):
    try:
        results = search(request.query, top_k=request.top_k)
        return SearchResponse(
            query=request.query,
            results=[SearchResult(**r) for r in results]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))