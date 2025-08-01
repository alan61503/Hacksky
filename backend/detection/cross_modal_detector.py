"""
Cross-modal inconsistency detection using CLIP and Whisper.
Detects inconsistencies between text, image, and audio content.
"""

import os
import tempfile
import logging
from typing import Dict, List, Optional, Tuple
import numpy as np
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import whisper

class CrossModalDetector:
    """
    Detects inconsistencies between text, image, and audio content using CLIP and Whisper.
    """
    
    def __init__(self):
        """Initialize the cross-modal detector with CLIP and Whisper models."""
        self.clip_model = None
        self.clip_processor = None
        self.whisper_model = None
        self._load_models()
    
    def _load_models(self):
        """Load CLIP and Whisper models."""
        try:
            print("🔄 Loading CLIP model for cross-modal detection...")
            self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            print("✅ CLIP model loaded successfully!")
            
            print("🔄 Loading Whisper model for audio transcription...")
            self.whisper_model = whisper.load_model("base")
            print("✅ Whisper model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            self.clip_model = None
            self.clip_processor = None
            self.whisper_model = None
    
    def analyze(self, text: str, image_path: Optional[str] = None, audio_path: Optional[str] = None) -> Dict:
        """
        Analyze cross-modal consistency between text, image, and audio.
        
        Args:
            text (str): Text content to analyze
            image_path (str, optional): Path to image file
            audio_path (str, optional): Path to audio file
            
        Returns:
            Dict: Analysis results with similarity scores and consistency assessment
        """
        results = {
            "text": text,
            "has_image": image_path is not None,
            "has_audio": audio_path is not None,
            "similarity_scores": {},
            "consistency_assessment": "unknown",
            "overall_trust_score": 50,
            "details": {}
        }
        
        try:
            # Process text-image similarity if image is provided
            if image_path and self.clip_model:
                text_image_similarity = self._analyze_text_image_similarity(text, image_path)
                results["similarity_scores"]["text_image"] = text_image_similarity
                results["details"]["text_image_analysis"] = f"Text-image similarity: {text_image_similarity:.2f}"
            
            # Process text-audio similarity if audio is provided
            if audio_path and self.whisper_model:
                text_audio_similarity = self._analyze_text_audio_similarity(text, audio_path)
                results["similarity_scores"]["text_audio"] = text_audio_similarity
                results["details"]["text_audio_analysis"] = f"Text-audio similarity: {text_audio_similarity:.2f}"
            
            # Calculate overall consistency and trust score
            consistency_assessment, overall_trust = self._calculate_consistency(results["similarity_scores"])
            results["consistency_assessment"] = consistency_assessment
            results["overall_trust_score"] = overall_trust
            
            # Add detailed reasoning
            results["details"]["reasoning"] = self._generate_consistency_reasoning(results)
            
        except Exception as e:
            logging.error(f"Error in cross-modal analysis: {e}")
            results["error"] = str(e)
            results["consistency_assessment"] = "error"
            results["overall_trust_score"] = 0
        
        return results
    
    def _analyze_text_image_similarity(self, text: str, image_path: str) -> float:
        """
        Analyze similarity between text and image using CLIP.
        
        Args:
            text (str): Text content
            image_path (str): Path to image file
            
        Returns:
            float: Similarity score between 0 and 1
        """
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            
            # Prepare inputs for CLIP
            inputs = self.clip_processor(
                text=[text],
                images=image,
                return_tensors="pt",
                padding=True,
                truncation=True
            )
            
            # Get embeddings
            with torch.no_grad():
                outputs = self.clip_model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=-1)
                
            # Return similarity score (probability of text matching image)
            similarity_score = probs[0][0].item()
            return similarity_score
            
        except Exception as e:
            logging.error(f"Error in text-image similarity analysis: {e}")
            return 0.5  # Neutral score on error
    
    def _analyze_text_audio_similarity(self, text: str, audio_path: str) -> float:
        """
        Analyze similarity between text and audio using Whisper transcription.
        
        Args:
            text (str): Text content
            audio_path (str): Path to audio file
            
        Returns:
            float: Similarity score between 0 and 1
        """
        try:
            # Transcribe audio
            result = self.whisper_model.transcribe(audio_path)
            audio_text = result["text"].strip().lower()
            
            # Simple text similarity using word overlap
            text_words = set(text.lower().split())
            audio_words = set(audio_text.split())
            
            if not text_words or not audio_words:
                return 0.0
            
            # Calculate Jaccard similarity
            intersection = len(text_words.intersection(audio_words))
            union = len(text_words.union(audio_words))
            
            similarity_score = intersection / union if union > 0 else 0.0
            
            return similarity_score
            
        except Exception as e:
            logging.error(f"Error in text-audio similarity analysis: {e}")
            return 0.5  # Neutral score on error
    
    def _calculate_consistency(self, similarity_scores: Dict[str, float]) -> Tuple[str, int]:
        """
        Calculate overall consistency assessment and trust score.
        
        Args:
            similarity_scores (Dict): Dictionary of similarity scores
            
        Returns:
            Tuple[str, int]: (consistency_assessment, trust_score)
        """
        if not similarity_scores:
            return "no_multimodal_content", 50
        
        # Calculate average similarity score
        avg_similarity = np.mean(list(similarity_scores.values()))
        
        # Determine consistency assessment
        if avg_similarity >= 0.7:
            consistency = "high_consistency"
            trust_score = int(80 + (avg_similarity - 0.7) * 100)
        elif avg_similarity >= 0.5:
            consistency = "moderate_consistency"
            trust_score = int(60 + (avg_similarity - 0.5) * 100)
        elif avg_similarity >= 0.3:
            consistency = "low_consistency"
            trust_score = int(30 + (avg_similarity - 0.3) * 100)
        else:
            consistency = "inconsistent"
            trust_score = int(avg_similarity * 100)
        
        # Clamp trust score to 0-100 range
        trust_score = max(0, min(100, trust_score))
        
        return consistency, trust_score
    
    def _generate_consistency_reasoning(self, results: Dict) -> str:
        """
        Generate human-readable reasoning for consistency assessment.
        
        Args:
            results (Dict): Analysis results
            
        Returns:
            str: Human-readable reasoning
        """
        consistency = results["consistency_assessment"]
        scores = results["similarity_scores"]
        
        if consistency == "high_consistency":
            return "Cross-modal analysis shows high consistency between text, image, and audio content. This suggests authentic, well-coordinated multimedia content."
        
        elif consistency == "moderate_consistency":
            return "Cross-modal analysis shows moderate consistency. Some discrepancies detected but content appears generally coherent."
        
        elif consistency == "low_consistency":
            return "Cross-modal analysis shows low consistency. Significant discrepancies detected between different modalities, suggesting potential manipulation."
        
        elif consistency == "inconsistent":
            return "Cross-modal analysis shows high inconsistency. Major discrepancies detected between text, image, and audio content. This may indicate manipulated or misleading content."
        
        elif consistency == "no_multimodal_content":
            return "No multimodal content provided for cross-modal analysis. Only text content was analyzed."
        
        else:
            return "Cross-modal analysis could not be completed due to technical issues."

def test_cross_modal_detector():
    """Test the cross-modal detector with sample content."""
    print("🧪 Testing Cross-Modal Detector...\n")
    
    detector = CrossModalDetector()
    
    # Test with text only
    print("📝 Test 1: Text-only analysis")
    result = detector.analyze("This is a test message about technology.")
    print(f"   Consistency: {result['consistency_assessment']}")
    print(f"   Trust Score: {result['overall_trust_score']}")
    print(f"   Reasoning: {result['details']['reasoning']}")
    print()
    
    # Test with text and image (if available)
    print("📝 Test 2: Text + Image analysis")
    # This would require an actual image file
    print("   (Image analysis would be performed with actual image file)")
    print()
    
    print("✅ Cross-modal detector test completed!")

if __name__ == "__main__":
    test_cross_modal_detector() 