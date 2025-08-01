
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import asyncio
import time
import os
import tempfile
import shutil

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

@app.post("/detect-cross-modal")
async def detect_cross_modal(
    text: str = Form(...),
    image: UploadFile = File(None),
    audio: UploadFile = File(None)
):
    """
    Analyze content with cross-modal inconsistency detection.
    Accepts text, image, and audio files for comprehensive analysis.
    """
    if not agent_instance:
        return {"error": "Agent not initialized"}
    
    try:
        # Create temporary files for uploaded content
        temp_files = []
        image_path = None
        audio_path = None
        
        # Save image file if provided
        if image:
            temp_image = tempfile.NamedTemporaryFile(delete=False, suffix=f".{image.filename.split('.')[-1]}")
            shutil.copyfileobj(image.file, temp_image)
            temp_image.close()
            image_path = temp_image.name
            temp_files.append(image_path)
        
        # Save audio file if provided
        if audio:
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio.filename.split('.')[-1]}")
            shutil.copyfileobj(audio.file, temp_audio)
            temp_audio.close()
            audio_path = temp_audio.name
            temp_files.append(audio_path)
        
        try:
            # Import the cross-modal analysis function
            from backend.detection.pipeline import analyze_post_with_cross_modal
            
            # Create post object
            post = {
                "id": agent_instance._post_id_counter,
                "author": "frontend_user",
                "content_type": "multimodal",
                "language": "en",
                "content": text,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            }
            
            # Analyze with cross-modal detection
            result = analyze_post_with_cross_modal(post, image_path, audio_path)
            
            # Increment counter
            agent_instance._post_id_counter += 1
            agent_instance.posts_processed += 1
            
            # Log the detection result
            from backend.logs.logger import log_detection
            log_detection(result)
            
            if DEBUG:
                log_system_event("CROSS_MODAL_ANALYSIS", f"📊 Cross-modal analysis completed for text: {text[:50]}...")
            
            return {
                "success": True,
                "post_id": result["post_id"],
                "trust_score": result["trust_score"],
                "reason": result.get("reason", "Cross-modal analysis completed"),
                "timestamp": result["timestamp"],
                "cross_modal_consistency": result.get("cross_modal_consistency", "unknown"),
                "similarity_scores": result.get("similarity_scores", {}),
                "cross_modal_details": result.get("cross_modal_analysis", {})
            }
            
        finally:
            # Clean up temporary files
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    except Exception as e:
        log_system_event("CROSS_MODAL_ERROR", f"❌ Error in cross-modal analysis: {str(e)}")
        return {"error": f"Cross-modal analysis failed: {str(e)}"}

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