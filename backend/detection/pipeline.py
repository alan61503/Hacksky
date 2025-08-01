# detection/pipeline.py
"""
Detection pipeline for analyzing posts and generating trust scores.
Now integrates with Hugging Face models for real misinformation detection.
"""

import random
import datetime
from typing import Dict

# Import the new Hugging Face detector
try:
    from backend.detection.huggingface_detector import analyze_text_with_huggingface
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False
    print("⚠️ Hugging Face detector not available. Using fallback analysis.")

# Import cross-modal detector
try:
    from backend.detection.cross_modal_detector import CrossModalDetector
    CROSS_MODAL_AVAILABLE = True
except ImportError:
    CROSS_MODAL_AVAILABLE = False
    print("⚠️ Cross-modal detector not available. Skipping cross-modal analysis.")

def analyze_post(post: Dict) -> Dict:
    """
    Analyze a post and generate a trust score with reasoning.
    
    Now uses Hugging Face zero-shot classification for real misinformation detection.
    Falls back to placeholder analysis if Hugging Face is not available.
    
    Args:
        post (Dict): Post dictionary containing id, content, content_type, etc.
        
    Returns:
        Dict: Analysis result with post_id, trust_score, reason, and timestamp
    """
    
    content = post.get("content", "")
    content_type = post.get("content_type", "text")
    
    # Use Hugging Face detector if available
    if HUGGINGFACE_AVAILABLE and content_type == "text":
        try:
            # Analyze with Hugging Face model
            analysis = analyze_text_with_huggingface(content)
            
            # Create result with Hugging Face analysis
            result = {
                "post_id": post["id"],
                "trust_score": analysis["trust_score"],
                "reason": analysis["reason"],
                "classification": analysis["classification"],
                "confidence": analysis["confidence"],
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Hugging Face analysis failed: {e}")
            # Fall back to placeholder analysis
    
    # Fallback to placeholder analysis
    trust_score = random.randint(0, 100)
    reason = _generate_reason(post, trust_score)
    
    result = {
        "post_id": post["id"],
        "trust_score": trust_score,
        "reason": reason,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    
    return result

def analyze_post_with_cross_modal(post: Dict, image_path: str = None, audio_path: str = None) -> Dict:
    """
    Analyze a post with cross-modal consistency detection.
    
    Args:
        post (Dict): Post dictionary containing id, content, content_type, etc.
        image_path (str, optional): Path to image file for cross-modal analysis
        audio_path (str, optional): Path to audio file for cross-modal analysis
        
    Returns:
        Dict: Analysis result with cross-modal consistency scores
    """
    
    # First, get the basic analysis
    basic_result = analyze_post(post)
    
    # Add cross-modal analysis if available
    if CROSS_MODAL_AVAILABLE and (image_path or audio_path):
        try:
            cross_modal_detector = CrossModalDetector()
            cross_modal_result = cross_modal_detector.analyze(
                text=post.get("content", ""),
                image_path=image_path,
                audio_path=audio_path
            )
            
            # Combine results
            combined_trust_score = _calculate_combined_trust_score(
                basic_result["trust_score"],
                cross_modal_result["overall_trust_score"]
            )
            
            # Update the result with cross-modal information
            basic_result.update({
                "cross_modal_analysis": cross_modal_result,
                "trust_score": combined_trust_score,
                "cross_modal_consistency": cross_modal_result["consistency_assessment"],
                "similarity_scores": cross_modal_result["similarity_scores"]
            })
            
        except Exception as e:
            print(f"❌ Cross-modal analysis failed: {e}")
            # Continue with basic analysis only
    
    return basic_result

def _calculate_combined_trust_score(text_trust: int, cross_modal_trust: int) -> int:
    """
    Calculate combined trust score from text analysis and cross-modal analysis.
    
    Args:
        text_trust (int): Trust score from text analysis (0-100)
        cross_modal_trust (int): Trust score from cross-modal analysis (0-100)
        
    Returns:
        int: Combined trust score (0-100)
    """
    # Weight cross-modal analysis more heavily if it's available
    # 40% text analysis + 60% cross-modal analysis
    combined_score = (text_trust * 0.4) + (cross_modal_trust * 0.6)
    return int(combined_score)

def _generate_reason(post: Dict, trust_score: int) -> str:
    """
    Generate a realistic reason string based on post content and trust score.
    This simulates what real ML model explanations might look like.
    
    Args:
        post (Dict): Post data
        trust_score (int): Generated trust score (0-100)
        
    Returns:
        str: Explanation for the trust score
    """
    
    content_type = post.get("content_type", "text")
    language = post.get("language", "en")
    content = post.get("content", "")
    
    # Define reason templates based on trust score ranges
    if trust_score >= 80:
        # High trust reasons
        high_trust_reasons = [
            f"Dummy analysis: High confidence authentic {content_type} content.",
            f"Placeholder: {content_type.title()} analysis shows strong credibility indicators.",
            f"Mock result: Language model confidence high for {language} {content_type}.",
            f"Test output: Content structure consistent with reliable {content_type} sources.",
            f"Simulated: Cross-reference check passed for {content_type} content."
        ]
        base_reason = random.choice(high_trust_reasons)
        
    elif trust_score >= 60:
        # Medium-high trust reasons
        medium_high_reasons = [
            f"Dummy analysis: Moderate confidence in {content_type} authenticity.",
            f"Placeholder: {content_type.title()} shows some credibility markers.",
            f"Mock result: {language} language patterns appear mostly natural.",
            f"Test output: Partial verification successful for {content_type}.",
            f"Simulated: Content quality acceptable but not exceptional."
        ]
        base_reason = random.choice(medium_high_reasons)
        
    elif trust_score >= 40:
        # Medium trust reasons
        medium_reasons = [
            f"Dummy analysis: Mixed signals detected in {content_type} content.",
            f"Placeholder: {content_type.title()} analysis shows conflicting indicators.",
            f"Mock result: {language} text patterns partially suspicious.",
            f"Test output: Inconclusive {content_type} verification results.",
            f"Simulated: Content requires human review for final determination."
        ]
        base_reason = random.choice(medium_reasons)
        
    elif trust_score >= 20:
        # Low trust reasons
        low_reasons = [
            f"Dummy analysis: Multiple red flags found in {content_type}.",
            f"Placeholder: {content_type.title()} shows suspicious patterns.",
            f"Mock result: {language} language model detects anomalies.",
            f"Test output: {content_type.title()} fails credibility checks.",
            f"Simulated: Content structure inconsistent with authentic sources."
        ]
        base_reason = random.choice(low_reasons)
        
    else:
        # Very low trust reasons
        very_low_reasons = [
            f"Dummy analysis: Strong misinformation indicators in {content_type}.",
            f"Placeholder: {content_type.title()} flagged as highly suspicious.",
            f"Mock result: {language} text shows clear manipulation signs.",
            f"Test output: {content_type.title()} fails multiple authenticity tests.",
            f"Simulated: Content matches known misinformation patterns."
        ]
        base_reason = random.choice(very_low_reasons)
    
    # Add specific content-based observations occasionally
    if random.random() < 0.3:  # 30% chance to add content observation
        content_observations = _get_content_observations(content, content_type)
        if content_observations:
            base_reason += f" {content_observations}"
    
    return base_reason

def _get_content_observations(content: str, content_type: str) -> str:
    """
    Generate content-specific observations for more realistic reasons.
    
    Args:
        content (str): Post content text
        content_type (str): Type of content (text, audio, video)
        
    Returns:
        str: Additional observation about the content
    """
    
    observations = []
    
    # Check for common misinformation keywords
    misinfo_keywords = [
        "BREAKING", "EXPOSED", "LEAKED", "SECRET", "HIDDEN", "SHOCKING",
        "REVEALED", "BOMBSHELL", "EXCLUSIVE", "URGENT", "DELETED",
        "Big Pharma", "mainstream media", "government", "conspiracy"
    ]
    
    keyword_count = sum(1 for keyword in misinfo_keywords if keyword.lower() in content.lower())
    
    if keyword_count >= 3:
        observations.append("High sensational language density detected.")
    elif keyword_count >= 1:
        observations.append("Some emotional manipulation indicators present.")
    
    # Check content length
    if len(content) > 200:
        observations.append("Lengthy content typical of misinformation posts.")
    elif len(content) < 50:
        observations.append("Brief content consistent with quick shares.")
    
    # Check for ALL CAPS usage
    caps_ratio = sum(1 for c in content if c.isupper()) / max(len(content), 1)
    if caps_ratio > 0.3:
        observations.append("Excessive capitalization suggests emotional manipulation.")
    
    # Check for urgency phrases
    urgency_phrases = ["SHARE", "DELETE", "BEFORE", "NOW", "URGENT", "QUICK"]
    if any(phrase in content.upper() for phrase in urgency_phrases):
        observations.append("Urgency tactics commonly used in misinformation.")
    
    # Content type specific observations
    if content_type == "video":
        video_obs = [
            "Video compression artifacts analysis pending.",
            "Temporal consistency check scheduled.",
            "Facial recognition patterns under review."
        ]
        observations.append(random.choice(video_obs))
    
    elif content_type == "audio":
        audio_obs = [
            "Voice pattern analysis in progress.",
            "Audio spectral analysis queued.",
            "Speech synthesis detection running."
        ]
        observations.append(random.choice(audio_obs))
    
    # Return random observation or empty string
    return random.choice(observations) if observations else ""

def get_pipeline_info() -> Dict:
    """
    Get information about the current pipeline configuration.
    Useful for monitoring and debugging.
    
    Returns:
        Dict: Pipeline metadata and configuration
    """
    return {
        "pipeline_version": "0.1.0-placeholder",
        "status": "placeholder_mode",
        "supported_content_types": ["text", "audio", "video"],
        "supported_languages": ["en", "es", "fr", "hi"],
        "ml_models": {
            "text_analysis": "placeholder - will use embeddings + classification",
            "audio_analysis": "placeholder - will use Whisper + sentiment analysis", 
            "video_analysis": "placeholder - will use CLIP + deepfake detection",
            "explainability": "placeholder - will use SHAP for interpretability"
        },
        "trust_score_range": "0-100 (integer)",
        "processing_time": "instant (placeholder) - will be ~1-5 seconds in production"
    }

# Test function to demonstrate the pipeline
def test_pipeline():
    """Test function to demonstrate post analysis."""
    print("🧪 Testing detection pipeline...\n")
    
    # Sample test posts
    test_posts = [
        {
            "id": 1,
            "author": "news_reporter2024",
            "content_type": "text",
            "language": "en",
            "content": "BREAKING: Scientists discover miracle cure for cancer - Big Pharma doesn't want you to know!",
            "timestamp": "2025-07-30T14:30:00.000000Z"
        },
        {
            "id": 2,
            "author": "local_journalist",
            "content_type": "video", 
            "language": "es",
            "content": "Local mayor announces new infrastructure project for downtown area.",
            "timestamp": "2025-07-30T14:31:00.000000Z"
        },
        {
            "id": 3,
            "author": "truth_seeker99",
            "content_type": "audio",
            "language": "fr", 
            "content": "EXPOSED: Government secretly tracking citizens through smartphones! SHARE BEFORE DELETED!",
            "timestamp": "2025-07-30T14:32:00.000000Z"
        }
    ]
    
    # Analyze each test post
    for post in test_posts:
        result = analyze_post(post)
        print(f"📊 Analysis Result for Post #{result['post_id']}:")
        print(f"   Trust Score: {result['trust_score']}/100")
        print(f"   Reason: {result['reason']}")
        print(f"   Analyzed at: {result['timestamp']}")
        print("-" * 80)
    
    # Show pipeline info
    print("\n🔧 Pipeline Information:")
    pipeline_info = get_pipeline_info()
    for key, value in pipeline_info.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for subkey, subvalue in value.items():
                print(f"     {subkey}: {subvalue}")
        else:
            print(f"   {key}: {value}")

if __name__ == "__main__":
    test_pipeline()