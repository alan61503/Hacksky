
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import asyncio
import time

from backend.agent import AutonomousAgent
from backend.logs.logger import log_system_event, get_logs, get_logs_summary, get_logs_by_trust_range
from backend.config import DEBUG, API_HOST, API_PORT

agent_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan: initialize agent on startup, cleanup on shutdown.
    """
    global agent_instance
    log_system_event("STARTUP", "Initializing autonomous AI agent...")
    agent_instance = AutonomousAgent()
    log_system_event("STARTUP", "🚀 Autonomous AI agent initialized successfully")
    try:
        yield
    finally:
        if agent_instance:
            log_system_event("SHUTDOWN", "🛑 Autonomous AI agent stopped")

app = FastAPI(
    title="Autonomous AI Misinformation Detection Engine",
    description="Real-time multimodal misinformation detection system",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """
    Root endpoint providing basic API information.
    """
    return {
        "message": "Autonomous AI Misinformation Detection Engine",
        "status": "running",
        "agent_active": agent_instance is not None,
        "debug_mode": DEBUG
    }

@app.post("/analyze")
async def analyze_content(content: str = Form(...), content_type: str = Form("text")):
    """
    Analyze content sent from frontend and return trust score and classification.
    """
    if not agent_instance:
        return {"error": "Agent not initialized"}
    
    try:
        result = agent_instance.analyze_content(content, content_type)
        return {
            "success": True,
            "post_id": result["post_id"],
            "trust_score": result["trust_score"],
            "reason": result["reason"],
            "timestamp": result["timestamp"]
        }
    except Exception as e:
        log_system_event("ANALYSIS_ERROR", f"❌ Error analyzing content: {str(e)}")
        return {"error": f"Analysis failed: {str(e)}"}

@app.get("/logs")
async def get_detection_logs(limit: int = 20):
    """
    Get recent detection logs for monitoring.
    """
    logs = get_logs(limit=limit)
    summary = get_logs_summary()
    
    return {
        "recent_logs": logs,
        "summary": summary,
        "total_logs_retrieved": len(logs)
    }

@app.get("/logs/low-trust")
async def get_low_trust_logs(limit: int = 10):
    """
    Get logs with low trust scores (potential misinformation).
    """
    logs = get_logs_by_trust_range(min_trust=0, max_trust=30, limit=limit)
    
    return {
        "low_trust_logs": logs,
        "total_low_trust": len(logs),
        "threshold": "0-30% trust score"
    }

@app.get("/status")
async def get_status():
    """
    Return current status of the autonomous agent and system health.
    """
    return {
        "agent_running": agent_instance is not None,
        "posts_processed": agent_instance.posts_processed if agent_instance else 0,
        "system_status": "healthy"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Autonomous AI Misinformation Detection Engine")
    print(f"📍 Host: {API_HOST}")
    print(f"🔌 Port: {API_PORT}")
    print(f"🐛 Debug: {DEBUG}")
    print("=" * 60)
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=DEBUG)