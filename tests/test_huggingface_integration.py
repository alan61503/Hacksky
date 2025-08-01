#!/usr/bin/env python3
"""
Test script to verify Hugging Face integration for misinformation detection.
"""

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_huggingface_import():
    """Test if Hugging Face dependencies are available."""
    print("🧪 Testing Hugging Face Integration...")
    
    try:
        import transformers
        import torch
        print("✅ Transformers and PyTorch imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("💡 Please install: pip install transformers torch")
        return False

def test_detector_creation():
    """Test creating the Hugging Face detector."""
    try:
        from backend.detection.huggingface_detector import HuggingFaceDetector
        print("🔄 Creating Hugging Face detector...")
        detector = HuggingFaceDetector()
        print("✅ Detector created successfully!")
        return detector
    except Exception as e:
        print(f"❌ Detector creation failed: {e}")
        return None

def test_text_analysis(detector):
    """Test analyzing sample text."""
    if not detector:
        return
    
    test_texts = [
        "COVID-19 vaccines are completely safe and effective for everyone.",
        "5G towers are causing coronavirus! Stay away from them!",
        "New study shows that exercise improves mental health.",
        "The government is hiding the truth about aliens!"
    ]
    
    print("\n📝 Testing text analysis:")
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. Text: {text[:50]}...")
        try:
            result = detector.analyze_text(text)
            print(f"   Trust Score: {result['trust_score']}%")
            print(f"   Classification: {result['classification']}")
            print(f"   Confidence: {result['confidence']}%")
            print(f"   Reason: {result['reason'][:100]}...")
        except Exception as e:
            print(f"   ❌ Analysis failed: {e}")

def test_pipeline_integration():
    """Test the full pipeline integration."""
    try:
        from backend.detection.pipeline import analyze_post
        
        test_post = {
            "id": 1,
            "content": "5G towers are causing coronavirus! Stay away from them!",
            "content_type": "text",
            "language": "en"
        }
        
        print("\n🔗 Testing pipeline integration:")
        result = analyze_post(test_post)
        
        print(f"   Post ID: {result['post_id']}")
        print(f"   Trust Score: {result['trust_score']}%")
        print(f"   Reason: {result['reason'][:100]}...")
        
        if 'classification' in result:
            print(f"   Classification: {result['classification']}")
            print(f"   Confidence: {result['confidence']}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Pipeline integration failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Hugging Face Integration Test Suite")
    print("=" * 50)
    
    # Test 1: Import dependencies
    if not test_huggingface_import():
        print("\n❌ Cannot proceed without Hugging Face dependencies.")
        print("💡 Run: pip install transformers torch")
        return
    
    # Test 2: Create detector
    detector = test_detector_creation()
    
    # Test 3: Analyze text
    test_text_analysis(detector)
    
    # Test 4: Pipeline integration
    test_pipeline_integration()
    
    print("\n🎉 Test suite completed!")
    print("\n📋 Next steps:")
    print("1. Start your backend: python -m uvicorn backend.main:app --reload")
    print("2. Open index.html in your browser")
    print("3. Create posts and watch for real Hugging Face analysis!")

if __name__ == "__main__":
    main() 