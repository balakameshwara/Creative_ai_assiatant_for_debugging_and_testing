from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from orchestrator import AgentOrchestrator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="AI SE Tool Backend")

# Initialize Orchestrator
orchestrator = AgentOrchestrator()

# Pydantic Models for Request Body
class CodeRequest(BaseModel):
    code: str
    context: Optional[str] = None

class DebugRequest(BaseModel):
    code: str
    error: str
    context: Optional[str] = None

class IngestRequest(BaseModel):
    file_paths: List[str]

# Endpoints

@app.get("/")
def health_check():
    return {"status": "running", "message": "AI SE Tool Backend is active."}

@app.post("/analyze")
def analyze_code(request: CodeRequest):
    """Performs code integrity check."""
    try:
        result = orchestrator.run_integrity_check(request.code)
        return {"analysis": result}
    except Exception as e:
        import traceback
        traceback.print_exc()
        if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
             raise HTTPException(status_code=429, detail="AI Model Rate Limit Exceeded. Please try again later.")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/debug")
def debug_code(request: DebugRequest):
    """Analyzes code and error to provide a fix."""
    try:
        result = orchestrator.run_debugger(request.code, request.error)
        return {"debug_info": result}
    except Exception as e:
        if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
             raise HTTPException(status_code=429, detail="AI Model Rate Limit Exceeded. Please try again later.")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test")
def generate_tests(request: CodeRequest):
    """Generates unit tests for the code."""
    try:
        result = orchestrator.run_tester(request.code)
        return {"tests": result}
    except Exception as e:
        if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
             raise HTTPException(status_code=429, detail="AI Model Rate Limit Exceeded. Please try again later.")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
def ingest_documents(request: IngestRequest):
    """Ingests file paths into the vector database."""
    try:
        valid_paths = [p for p in request.file_paths if os.path.exists(p)]
        if not valid_paths:
            return {"message": "No valid file paths found."}
        
        orchestrator.ingest_files(valid_paths)
        return {"message": f"Successfully ingested {len(valid_paths)} files."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
