import json
import time
import uuid
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from src.agent import PractoLangGraphAgent
from src.guardrails import GuardrailEngine

app = FastAPI(title="Practo Support Agent Backend")
agent = PractoLangGraphAgent()
LOG_PATH = "data/logs.jsonl"
os.makedirs("data", exist_ok=True)

class QueryRequest(BaseModel):
    query: str
    appointment_id: Optional[str] = None

class DocumentRequest(BaseModel):
    filename: str
    content: str

def log_request(trace_id: str, raw_query: str, duration_ms: float):
    # Task 12: Ensure raw phone numbers/emails never reach disk in logs
    sanitized_query = GuardrailEngine.mask_pii(raw_query)
    log_entry = {
        "trace_id": trace_id,
        "sanitized_query": sanitized_query,
        "duration_ms": round(duration_ms, 2),
        "timestamp": time.time()
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

@app.post("/ask")
def ask_endpoint(req: QueryRequest):
    start = time.time()
    trace_id = str(uuid.uuid4())
    res = agent.run(query=req.query, appointment_id=req.appointment_id)
    duration_ms = (time.time() - start) * 1000.0
    
    log_request(trace_id, req.query, duration_ms)
    return {
        "trace_id": trace_id,
        "response": res["final_response"],
        "sources": res.get("sources", []),
        "route_taken": res.get("route")
    }

@app.post("/add-document")
def add_document_endpoint(req: DocumentRequest):
    path = os.path.join("data/kb_documents", req.filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(req.content)
    agent.vsm.ingesting_kb(strategy="fixed_size")
    return {"status": "success", "message": f"Added document {req.filename}"}