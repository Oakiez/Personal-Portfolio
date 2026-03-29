from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import random

app = FastAPI(title="AI Service", version="1.0.0")

class AnalysisPayload(BaseModel):
    file_id: str
    filename: str
    word_count: int
    char_count: int
    content_preview: str = ""

def mock_sentiment(text: str) -> str:
    if not text:
        return "neutral"
    positive_words = ["good", "great", "success", "ok", "healthy"]
    negative_words = ["error", "fail", "bad", "broken"]
    text_lower = text.lower()
    if any(w in text_lower for w in positive_words):
        return "positive"
    if any(w in text_lower for w in negative_words):
        return "negative"
    return "neutral"

def mock_category(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "unknown"
    categories = {
        "txt": "text_document",
        "pdf": "pdf_document",
        "csv": "data_file",
        "json": "structured_data",
        "py": "source_code",
        "log": "log_file"
    }
    return categories.get(ext, "generic_file")

@app.get("/health")
async def health():
    return {"service": "ai_service", "status": "online", "port": 8002}

@app.post("/analyze")
async def analyze(payload: AnalysisPayload):
    sentiment = mock_sentiment(payload.content_preview)
    category = mock_category(payload.filename)
    confidence = round(random.uniform(0.75, 0.99), 2)

    return JSONResponse({
        "status": "analyzed",
        "file_id": payload.file_id,
        "filename": payload.filename,
        "ai_results": {
            "category": category,
            "sentiment": sentiment,
            "confidence": confidence,
            "word_count": payload.word_count,
            "summary": f"File '{payload.filename}' classified as '{category}' with {confidence*100:.0f}% confidence."
        }
    })

@app.get("/")
async def root():
    return {"service": "AI Service", "version": "1.0.0", "endpoints": ["/health", "/analyze"]}
