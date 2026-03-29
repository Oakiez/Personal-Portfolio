from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import httpx
import os
import uuid

app = FastAPI(title="Gateway Service", version="1.0.0")

UPLOAD_SERVICE_URL   = os.getenv("UPLOAD_SERVICE_URL",   "http://localhost:8000")
PROCESSING_SERVICE_URL = os.getenv("PROCESSING_SERVICE_URL", "http://localhost:8001")
AI_SERVICE_URL       = os.getenv("AI_SERVICE_URL",       "http://localhost:8002")

@app.get("/health")
async def health():
    services = {}
    async with httpx.AsyncClient(timeout=5.0) as client:
        for name, url in [
            ("upload",     UPLOAD_SERVICE_URL),
            ("processing", PROCESSING_SERVICE_URL),
            ("ai",         AI_SERVICE_URL),
        ]:
            try:
                r = await client.get(f"{url}/health")
                services[name] = r.json()
            except Exception as e:
                services[name] = {"status": "unreachable", "error": str(e)}

    all_ok = all(s.get("status") == "online" for s in services.values())
    return JSONResponse({
        "gateway": "online",
        "overall_status": "healthy" if all_ok else "degraded",
        "services": services
    })

@app.post("/process-file")
async def process_file_workflow(file: UploadFile = File(...)):
    """Full pipeline: Upload → Processing → AI → Response"""
    file_id = str(uuid.uuid4())
    content = await file.read()

    async with httpx.AsyncClient(timeout=15.0) as client:
        # Step 1: Processing
        try:
            proc_resp = await client.post(
                f"{PROCESSING_SERVICE_URL}/process",
                json={
                    "file_id": file_id,
                    "filename": file.filename,
                    "size": len(content),
                    "content_preview": content[:300].decode("utf-8", errors="ignore")
                }
            )
            proc_result = proc_resp.json()
        except Exception as e:
            proc_result = {"error": str(e)}

        # Step 2: AI
        try:
            ai_resp = await client.post(
                f"{AI_SERVICE_URL}/analyze",
                json={
                    "file_id": file_id,
                    "filename": file.filename,
                    "word_count": len(content.split()) if isinstance(content, bytes) else 0,
                    "char_count": len(content),
                    "content_preview": content[:300].decode("utf-8", errors="ignore")
                }
            )
            ai_result = ai_resp.json()
        except Exception as e:
            ai_result = {"error": str(e)}

    return JSONResponse({
        "gateway": "process-file",
        "file_id": file_id,
        "filename": file.filename,
        "pipeline": {
            "processing": proc_result,
            "ai": ai_result
        },
        "status": "complete"
    })

@app.get("/")
async def root():
    return {
        "service": "Gateway Service",
        "version": "1.0.0",
        "endpoints": ["/health", "/process-file"],
        "routes_to": {
            "upload": UPLOAD_SERVICE_URL,
            "processing": PROCESSING_SERVICE_URL,
            "ai": AI_SERVICE_URL
        }
    }
