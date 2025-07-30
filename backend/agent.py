# backend/agent.py - Updated for frontend-driven analysis

import asyncio
import time
from typing import Optional

# Fixed imports for backend/ directory
from backend.feed.fake_feed import generate_fake_post
from backend.detection.pipeline import analyze_post
from backend.logs.logger import log_detection, log_system_event
from backend.config import DEBUG

class AutonomousAgent:
    """
    AI agent that analyzes content for misinformation detection.
    Now processes content sent from frontend instead of generating fake posts.
    """
    
    def __init__(self):
        """Initialize the agent with required components."""
        self.posts_processed = 0
        self._post_id_counter = 1
    
    def analyze_content(self, content: str, content_type: str = "text") -> dict:
        """
        Analyze content sent from frontend and return detection results.
        
        Args:
            content (str): The content to analyze
            content_type (str): Type of content (text, audio, video, image)
            
        Returns:
            dict: Analysis result with post_id, trust_score, reason, and timestamp
        """
        # Create a post object for the detection pipeline
        post = {
            "id": self._post_id_counter,
            "author": "frontend_user",
            "content_type": content_type,
            "language": "en",  # Default to English
            "content": content,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        }
        
        # Increment counter for next post
        self._post_id_counter += 1
        
        # Process through detection pipeline
        detection_result = analyze_post(post)
        
        # Log the detection result
        log_detection(detection_result)
        
        self.posts_processed += 1
        
        if DEBUG:
            content_preview = content[:50] + "..." if len(content) > 50 else content
            log_system_event("ANALYSIS", f"📝 Analyzed content: {content_preview}")
        
        return detection_result

if __name__ == "__main__":
    # Test the agent
    agent = AutonomousAgent()
    test_content = "This is a test message to verify the detection pipeline works."
    result = agent.analyze_content(test_content, "text")
    print(f"Test result: {result}")