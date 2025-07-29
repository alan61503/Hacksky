
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from backend.agent import AutonomousAgent
from backend.logs.logger import log_system_event, get_logs, get_logs_summary
from backend.config import AGENT_INTERVAL, DEBUG, API_HOST, API_PORT

agent_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan: start agent on startup, stop on shutdown.
    """
    global agent_instance
    log_system_event("STARTUP", "Initializing autonomous AI agent...")
    agent_instance = AutonomousAgent()
    agent_task = asyncio.create_task(agent_instance.start())
    log_system_event("STARTUP", "🚀 Autonomous AI agent started successfully")
    try:
        yield
    finally:
        if agent_instance:
            await agent_instance.stop()
            agent_task.cancel()
            try:
                await agent_task
            except asyncio.CancelledError:
                pass
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
        "agent_active": agent_instance.is_running if agent_instance else False,
        "debug_mode": DEBUG
    }

@app.get("/logs")
async def get_logs_endpoint():
    """
    Retrieve recent detection logs and summary.
    """
    logs = get_logs(limit=20)
    summary = get_logs_summary()
    return {
        "logs": logs,
        "summary": summary,
        "total_returned": len(logs)
    }

@app.get("/status")
async def get_status():
    """
    Return current status of the autonomous agent and system health.
    """
    return {
        "agent_running": agent_instance.is_running if agent_instance else False,
        "posts_processed": agent_instance.posts_processed if agent_instance else 0,
        "uptime_seconds": agent_instance.get_uptime() if agent_instance else 0,
        "system_status": "healthy",
        "agent_interval": AGENT_INTERVAL
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=DEBUG)