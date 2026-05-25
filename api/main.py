from fastapi import FastAPI
from api.routers import notes

app = FastAPI(
    title="MediSummarize API",
    description="Clinical note summarisation and search",
    version="0.1.0"
)

app.include_router(notes.router)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}