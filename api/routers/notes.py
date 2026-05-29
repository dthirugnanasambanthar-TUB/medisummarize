import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../rag'))

from fastapi import APIRouter, HTTPException, Depends
from api.schema import (
    SummariseRequest, SOAPResponse,
    SearchRequest, SearchResponse, SearchResult
)
from api.auth import get_current_user
from rag.summariser import summarise_note
from rag.retriever import search
from workers.tasks import summarise_note_task
from celery.result import AsyncResult

router = APIRouter(prefix="/api/v1", tags=["notes"])

@router.post("/summarise", response_model=SOAPResponse)
async def summarise(
    request: SummariseRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        summary = summarise_note(request.note_id)
        return SOAPResponse(note_id=request.note_id, **summary.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=SearchResponse)
async def search_notes(
    request: SearchRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        results = search(request.query, top_k=request.top_k)
        return SearchResponse(
            query=request.query,
            results=[SearchResult(**r) for r in results]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarise/async")
async def summarise_async(
    request: SummariseRequest,
    current_user: dict = Depends(get_current_user)
):
    task = summarise_note_task.delay(request.note_id)
    return {
        "task_id": task.id,
        "status": "queued",
        "message": f"Summarisation job queued for {request.note_id}"
    }

@router.get("/tasks/{task_id}")
async def get_task_status(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    task = AsyncResult(task_id)
    if task.state == "PENDING":
        return {"task_id": task_id, "status": "pending"}
    elif task.state == "STARTED":
        return {"task_id": task_id, "status": "processing"}
    elif task.state == "SUCCESS":
        return {"task_id": task_id, "status": "complete", "result": task.result}
    elif task.state == "FAILURE":
        return {"task_id": task_id, "status": "failed", "error": str(task.result)}
    else:
        return {"task_id": task_id, "status": task.state}