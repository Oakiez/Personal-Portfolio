from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx
import os

app = FastAPI(title="Processing Service", version="1.0.0")

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:8002")

class FilePayload(BaseModel):
    file_id: str
    filename: str
    size: int
    content_preview: str = ""

@app.get("/health")
async def health():
    return {"service": "processing_service", "status": "online", "port": 8001}

@app.post("/process")
async def process_file(payload: FilePayload):
    # Simulate processing
    word_count = len(payload.content_preview.split())
    char_count = len(payload.content_preview)

    # Forward to AI service
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{AI_SERVICE_URL}/analyze",
                json={
                    "file_id": payload.file_id,
                    "filename": payload.filename,
                    "word_count": word_count,
                    "char_count": char_count,
                    "content_preview": payload.content_preview
                }
            )
            ai_result = response.json()
    except Exception as e:
        ai_result = {"error": str(e), "status": "ai_unavailable"}

    return JSONResponse({
        "status": "processed",
        "file_id": payload.file_id,
        "filename": payload.filename,
        "metrics": {
            "word_count": word_count,
            "char_count": char_count,
            "size_bytes": payload.size
        },
        "ai_analysis": ai_result
    })

@app.get("/")
async def root():
    return {"service": "Processing Service", "version": "1.0.0", "endpoints": ["/health", "/process"]}
