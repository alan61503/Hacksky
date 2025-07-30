# backend/agent.py - Fixed for backend/ directory structure

import asyncio
import time
from typing import Optional

# Fixed imports for backend/ directory
from backend.feed.fake_feed import generate_fake_post
from backend.detection.pipeline import analyze_post
from backend.logs.logger import log_detection, log_system_event
from backend.config import settings

class AutonomousAgent:
    """
    Autonomous AI agent that continuously monitors and analyzes content
    for misinformation detection in real-time.
    """
    
    def __init__(self):
        """Initialize the autonomous agent with required components."""
        self.is_running = False
        self.posts_processed = 0
        self.start_time: Optional[float] = None
        self._stop_event = asyncio.Event()
    
    async def start(self):
        """
        Start the autonomous agent loop. Generates fake posts every AGENT_INTERVAL seconds
        and processes them through the detection pipeline.
        """
        self.is_running = True
        self.start_time = time.time()
        log_system_event("AGENT", "🤖 Autonomous agent started - beginning content analysis")
        
        try:
            while not self._stop_event.is_set():
                try:
                    # Generate a fake post
                    fake_post = generate_fake_post()
                    
                    if DEBUG:
                        content_preview = fake_post['content'][:50] + "..." if len(fake_post['content']) > 50 else fake_post['content']
                        log_system_event("AGENT", f"📝 Generated post #{fake_post['id']}: {content_preview}")
                    
                    # Process through detection pipeline
                    detection_result = analyze_post(fake_post)
                    
                    # Log the detection result
                    log_detection(detection_result)
                    
                    self.posts_processed += 1
                    
                    # Wait for the configured interval
                    try:
                        await asyncio.wait_for(
                            self._stop_event.wait(), 
                            timeout=AGENT_INTERVAL
                        )
                        break  # Stop event was set
                    except asyncio.TimeoutError:
                        continue  # Continue the loop
                        
                except Exception as e:
                    log_system_event("AGENT_ERROR", f"❌ Error in agent loop: {str(e)}")
                    await asyncio.sleep(1)  # Brief pause before retrying
                    
        except asyncio.CancelledError:
            log_system_event("AGENT", "🛑 Agent loop cancelled")
        finally:
            self.is_running = False
    
    async def stop(self):
        """Gracefully stop the autonomous agent loop."""
        log_system_event("AGENT", "⏹️ Stopping autonomous agent...")
        self._stop_event.set()
        self.is_running = False
    
    def get_uptime(self) -> float:
        """
        Get the agent uptime in seconds.
        
        Returns:
            float: Uptime in seconds, or 0 if not started
        """
        if self.start_time:
            return time.time() - self.start_time
        return 0.0