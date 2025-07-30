"""
Hugging Face-based misinformation detection using zero-shot classification.
Uses facebook/bart-large-mnli model for real-time content analysis.
"""

from transformers import pipeline
import logging
from typing import Dict, List, Optional
import time

class HuggingFaceDetector:
    """
    Real misinformation detection using Hugging Face zero-shot classification.
    """
    
    def __init__(self):
        """Initialize the Hugging Face zero-shot classifier."""
        self.classifier = None
        self.labels = [
            "misinformation",
            "credible information", 
            "satire or humor",
            "clickbait",
            "conspiracy theory",
            "factual news"
        ]
        self._load_model()
    
    def _load_model(self):
        """Load the zero-shot classification model."""
        try:
            print("🔄 Loading Hugging Face zero-shot classifier...")
            self.classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1  # Use CPU (-1), change to 0 for GPU
            )
            print("✅ Hugging Face model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading Hugging Face model: {e}")
            print("💡 Make sure to install: pip install transformers torch")
            self.classifier = None
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze text for misinformation using zero-shot classification.
        
        Args:
            text (str): Text content to analyze
            
        Returns:
            Dict: Analysis result with trust score and classification
        """
        if not self.classifier:
            return self._fallback_analysis(text)
        
        try:
            # Run zero-shot classification
            result = self.classifier(text, self.labels)
            
            # Extract the most likely label and its confidence
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            
            # Calculate trust score based on classification
            trust_score = self._calculate_trust_score(top_label, top_score)
            
            # Generate detailed reason
            reason = self._generate_reason(top_label, top_score, result)
            
            return {
                "trust_score": trust_score,
                "classification": top_label,
                "confidence": round(top_score * 100, 1),
                "reason": reason,
                "all_scores": dict(zip(result['labels'], [round(s * 100, 1) for s in result['scores']]))
            }
            
        except Exception as e:
            print(f"❌ Error in Hugging Face analysis: {e}")
            return self._fallback_analysis(text)
    
    def _calculate_trust_score(self, label: str, confidence: float) -> int:
        """
        Calculate trust score (0-100) based on classification and confidence.
        
        Args:
            label (str): Predicted label
            confidence (float): Model confidence (0-1)
            
        Returns:
            int: Trust score from 0-100
        """
        # Base trust scores for different labels
        base_scores = {
            "credible information": 85,
            "factual news": 90,
            "satire or humor": 60,
            "clickbait": 30,
            "conspiracy theory": 15,
            "misinformation": 10
        }
        
        # Get base score for the label
        base_score = base_scores.get(label, 50)
        
        # Adjust based on confidence
        confidence_factor = confidence * 0.3  # Confidence can adjust score by ±30%
        
        # Calculate final score
        final_score = base_score + (confidence_factor * 100) - 15
        
        # Clamp to 0-100 range
        return max(0, min(100, int(final_score)))
    
    def _generate_reason(self, label: str, confidence: float, result: Dict) -> str:
        """
        Generate a human-readable reason for the classification.
        
        Args:
            label (str): Predicted label
            confidence (float): Model confidence
            result (Dict): Full classification result
            
        Returns:
            str: Human-readable reason
        """
        confidence_pct = round(confidence * 100, 1)
        
        if label == "misinformation":
            return f"AI model classified as misinformation with {confidence_pct}% confidence. Multiple indicators suggest this content may be false or misleading."
        
        elif label == "conspiracy theory":
            return f"Content matches conspiracy theory patterns with {confidence_pct}% confidence. Claims appear to be unsubstantiated."
        
        elif label == "clickbait":
            return f"Detected as clickbait with {confidence_pct}% confidence. Content uses sensationalist language to attract attention."
        
        elif label == "satire or humor":
            return f"Classified as satire/humor with {confidence_pct}% confidence. Content appears to be intentionally humorous or satirical."
        
        elif label == "credible information":
            return f"Classified as credible information with {confidence_pct}% confidence. Content appears to be factual and well-sourced."
        
        elif label == "factual news":
            return f"Classified as factual news with {confidence_pct}% confidence. Content appears to be legitimate news reporting."
        
        else:
            return f"Classified as '{label}' with {confidence_pct}% confidence."
    
    def _fallback_analysis(self, text: str) -> Dict:
        """
        Fallback analysis when Hugging Face model is not available.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict: Basic analysis result
        """
        # Simple keyword-based fallback
        text_lower = text.lower()
        
        # Misinformation indicators
        misinformation_keywords = [
            "conspiracy", "fake news", "hoax", "cover up", "they don't want you to know",
            "miracle cure", "secret", "hidden truth", "government hiding", "mainstream media lies"
        ]
        
        # Credible indicators
        credible_keywords = [
            "study shows", "research indicates", "according to", "scientists say",
            "peer-reviewed", "evidence suggests", "data shows"
        ]
        
        # Count indicators
        misinfo_count = sum(1 for keyword in misinformation_keywords if keyword in text_lower)
        credible_count = sum(1 for keyword in credible_keywords if keyword in text_lower)
        
        # Calculate basic trust score
        if misinfo_count > credible_count:
            trust_score = max(10, 50 - (misinfo_count * 10))
            classification = "misinformation"
            reason = f"Fallback analysis: Found {misinfo_count} misinformation indicators"
        elif credible_count > misinfo_count:
            trust_score = min(90, 50 + (credible_count * 10))
            classification = "credible information"
            reason = f"Fallback analysis: Found {credible_count} credible indicators"
        else:
            trust_score = 50
            classification = "uncertain"
            reason = "Fallback analysis: Mixed indicators, unable to determine"
        
        return {
            "trust_score": trust_score,
            "classification": classification,
            "confidence": 50.0,
            "reason": reason,
            "all_scores": {"fallback": 100.0}
        }

# Global instance for reuse
_detector_instance = None

def get_detector() -> HuggingFaceDetector:
    """Get or create the global detector instance."""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = HuggingFaceDetector()
    return _detector_instance

def analyze_text_with_huggingface(text: str) -> Dict:
    """
    Analyze text using Hugging Face model.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        Dict: Analysis result
    """
    detector = get_detector()
    return detector.analyze_text(text)

# Test function
def test_huggingface_detector():
    """Test the Hugging Face detector with sample content."""
    print("🧪 Testing Hugging Face Misinformation Detector...\n")
    
    test_texts = [
        "COVID-19 vaccines are completely safe and effective for everyone.",
        "5G towers are causing coronavirus! Stay away from them!",
        "New study shows that exercise improves mental health.",
        "The government is hiding the truth about aliens!",
        "Scientists discover new species in the Amazon rainforest.",
        "This miracle cure will solve all your problems!"
    ]
    
    detector = HuggingFaceDetector()
    
    for i, text in enumerate(test_texts, 1):
        print(f"📝 Test {i}: {text[:50]}...")
        result = detector.analyze_text(text)
        
        print(f"   Trust Score: {result['trust_score']}%")
        print(f"   Classification: {result['classification']}")
        print(f"   Confidence: {result['confidence']}%")
        print(f"   Reason: {result['reason']}")
        print()

if __name__ == "__main__":
    test_huggingface_detector() 