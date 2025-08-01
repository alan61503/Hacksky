# 🤗 Hugging Face Integration Setup

This guide will help you set up real misinformation detection using Hugging Face models.

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install transformers torch accelerate
```

### 2. Test the Integration
```bash
python test_huggingface_integration.py
```

### 3. Start Your Backend
```bash
python -m uvicorn backend.main:app --reload
```

### 4. Test with Frontend
- Open `index.html` in your browser
- Create posts and watch the terminal for real AI analysis!

## 🔧 What's New

### Real AI Detection
- **Model**: `facebook/bart-large-mnli` (zero-shot classification)
- **Labels**: misinformation, credible information, satire, clickbait, conspiracy theory, factual news
- **Fallback**: Keyword-based analysis if Hugging Face is unavailable

### Enhanced Analysis
- **Trust Score**: 0-100% based on AI classification
- **Confidence**: Model confidence percentage
- **Classification**: Specific category (misinformation, credible, etc.)
- **Detailed Reasons**: Human-readable explanations

## 📊 Example Output

```
[AI-Agent] Post #1 → Trust Score: 15% 🚨 → Reason: AI model classified as conspiracy theory with 87.3% confidence. Claims appear to be unsubstantiated.
[AI-Agent] Post #2 → Trust Score: 85% ✅ → Reason: Classified as credible information with 92.1% confidence. Content appears to be factual and well-sourced.
```

## 🛠️ Files Modified

- `backend/detection/huggingface_detector.py` - New AI detector
- `backend/detection/pipeline.py` - Updated to use Hugging Face
- `backend/requirements.txt` - Added AI dependencies
- `test_huggingface_integration.py` - Test script

## 🔍 Troubleshooting

### "ModuleNotFoundError: No module named 'transformers'"
```bash
pip install transformers torch
```

### "CUDA out of memory" (GPU users)
The model uses CPU by default. For GPU, change `device=-1` to `device=0` in `huggingface_detector.py`.

### Slow first analysis
The model downloads on first use (~1.5GB). Subsequent analyses will be faster.

## 🎯 Next Steps

1. **Test with real content** - Try posting various types of content
2. **Monitor logs** - Watch the terminal for live detection results
3. **Customize labels** - Modify the classification labels in `huggingface_detector.py`
4. **Add more models** - Integrate additional Hugging Face models for different content types

## 📈 Performance

- **First run**: ~10-30 seconds (model download)
- **Subsequent runs**: ~1-3 seconds per analysis
- **Memory usage**: ~2-3GB RAM
- **CPU usage**: Moderate (single-threaded)

---

**Ready to detect real misinformation! 🚀** 