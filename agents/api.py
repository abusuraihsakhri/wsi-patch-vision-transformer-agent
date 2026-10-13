"""
FastAPI REST API Server for Wsi Patch Vision Transformer Agent.
"""
from pathlib import Path
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard, SecurityException
from .models import SystemTaskPayload, ConsensusDossier, UrgencyLevel
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Wsi Patch Vision Transformer Agent API",
    description="Enterprise Distributed Component Platform (Digital Pathology & Histology Systems)",
    version="3.0.0-ENTERPRISE",
)


class ChatRequest(BaseModel):
    query: str


WEB_DIR = Path(__file__).resolve().parent.parent / "web"


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/app.mjs", include_in_schema=False)
def browser_script():
    return FileResponse(WEB_DIR / "app.mjs", media_type="text/javascript")


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "wsi-patch-vision-transformer-agent", "domain": "Digital Pathology & Histology Systems", "standard": "CAP Cancer Protocols / DICOM WSI PS3.16", "version": "3.0.0-ENTERPRISE"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "OPERATIONAL"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    try:
        dossier = supervisor.process_task(payload)
    except SecurityException:
        raise HTTPException(status_code=422, detail="Potential personal identifier detected; use synthetic identifiers.")
    return dossier.to_dict()


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except SecurityException:
        raise HTTPException(status_code=422, detail="Potential personal identifier detected; use synthetic identifiers.")


@app.get("/api/audit/logs")
def api_audit_logs():
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
