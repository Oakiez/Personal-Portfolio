from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import httpx
import os
import uuid

app = FastAPI(title="Upload Service", version="1.0.0")

PROCESSING_SERVICE_URL = os.getenv("PROCESSING_SERVICE_URL", "http://localhost:8001")

@app.get("/health")
async def health():
    return {"service": "upload_service", "status": "online", "port": 8000}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    content = await file.read()
    file_size = len(content)

    # Forward to processing service
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{PROCESSING_SERVICE_URL}/process",
                json={
                    "file_id": file_id,
                    "filename": file.filename,
                    "size": file_size,
                    "content_preview": content[:200].decode("utf-8", errors="ignore")
                }
            )
            processing_result = response.json()
    except Exception as e:
        processing_result = {"error": str(e), "status": "processing_unavailable"}

    return JSONResponse({
        "status": "uploaded",
        "file_id": file_id,
        "filename": file.filename,
        "size_bytes": file_size,
        "processing": processing_result
    })

@app.get("/")
async def root():
    return {"service": "Upload Service", "version": "1.0.0", "endpoints": ["/health", "/upload"]}
