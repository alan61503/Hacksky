# Autonomous AI Misinformation Detection Engine

A FastAPI-based backend system that continuously monitors and analyzes content for misinformation detection using AI/ML techniques.

## 🚀 Features

### 🤖 **Autonomous AI Agent**
- Continuously generates and analyzes fake posts for testing
- Real-time content monitoring and processing
- Configurable analysis intervals
- Graceful startup and shutdown

### 🔍 **Detection Pipeline**
- Multi-modal content analysis (text, image, video, audio)
- Trust score generation (0-100%)
- Explainable AI reasoning
- Placeholder for real ML models (Whisper, CLIP, etc.)

### 📊 **Logging & Monitoring**
- Real-time detection logs
- System event tracking
- Performance metrics
- Memory-based storage (ready for MongoDB)

### 🌐 **FastAPI REST API**
- Health check endpoints
- Real-time status monitoring
- Log retrieval and analysis
- Interactive API documentation

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run tests to verify setup:**
   ```bash
   python test_backend.py
   ```

3. **Start the server:**
   ```bash
   python run.py
   # or
   python main.py
   ```

## 📡 API Endpoints

### Base URL: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and status |
| `/status` | GET | Agent and system health |
| `/logs` | GET | Recent detection logs |
| `/docs` | GET | Interactive API documentation |

### Example API Usage

```bash
# Get API status
curl http://localhost:8000/

# Check agent status
curl http://localhost:8000/status

# Get recent logs
curl http://localhost:8000/logs
```

## 🔧 Configuration

Configuration is handled in `config.py` with environment variable support:

```python
# Agent Configuration
AGENT_LOOP_INTERVAL: float = 2.0  # seconds between posts
DEBUG: bool = True                # enable debug logs

# API Configuration  
API_HOST: str = "0.0.0.0"
API_PORT: int = 8000
```

### Environment Variables
Create a `.env` file to override defaults:
```env
AGENT_LOOP_INTERVAL=5.0
DEBUG=false
API_HOST=127.0.0.1
API_PORT=8080
```

## 🏗️ Architecture

```
backend/
├── main.py              # FastAPI application entry point
├── agent.py             # Autonomous AI agent
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── run.py              # Server startup script
├── test_backend.py     # Comprehensive test suite
├── feed/
│   └── fake_feed.py    # Fake content generator
├── detection/
│   └── pipeline.py     # AI detection pipeline
└── logs/
    └── logger.py       # Logging system
```

## 🧪 Testing

### Run All Tests
```bash
python test_backend.py
```

### Test Components Individually
```python
# Test fake feed generation
from backend.feed.fake_feed import generate_fake_post
post = generate_fake_post()
print(post)

# Test detection pipeline
from backend.detection.pipeline import analyze_post
result = analyze_post(post)
print(result)

# Test logging
from backend.logs.logger import log_detection
log_detection(result)
```

## 🔄 Development Workflow

1. **Start the server:**
   ```bash
   python run.py
   ```

2. **Monitor logs in real-time:**
   - Watch console output for agent activity
   - Check `/logs` endpoint for detection results

3. **Test API endpoints:**
   - Visit `http://localhost:8000/docs` for interactive docs
   - Use curl or Postman to test endpoints

4. **Modify and reload:**
   - Changes to Python files auto-reload (DEBUG=True)
   - Agent restarts automatically

## 🚨 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Install dependencies
pip install -r requirements.txt
```

**Port Already in Use:**
```bash
# Change port in config.py or .env
API_PORT=8080
```

**Agent Not Starting:**
```bash
# Check logs for errors
# Verify all modules can be imported
python test_backend.py
```

### Debug Mode
Set `DEBUG=True` in config for:
- Detailed console logging
- Auto-reload on file changes
- Extended error messages

## 🔮 Future Enhancements

### Planned Features
- **Real ML Models**: Integrate Whisper, CLIP, BERT
- **Database Integration**: MongoDB for persistent storage
- **Real-time Streaming**: WebSocket connections
- **Advanced Analytics**: Detection trends and patterns
- **User Management**: Authentication and authorization
- **Content Sources**: Real social media API integration

### AI Model Integration
```python
# Future: Real ML model integration
from transformers import pipeline
from openai import OpenAI

# Text analysis
text_analyzer = pipeline("text-classification")

# Image analysis  
image_analyzer = pipeline("image-classification")

# Audio transcription
audio_transcriber = pipeline("automatic-speech-recognition")
```

## 📊 Performance

### Current Performance
- **Posts per second**: ~0.5 (configurable)
- **Memory usage**: ~50MB
- **Response time**: <100ms for API calls
- **Uptime**: Continuous operation

### Optimization Opportunities
- Async processing for multiple posts
- Caching for repeated analysis
- Database indexing for log queries
- Model optimization and quantization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python test_backend.py`
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

**Ready to detect misinformation with AI! 🤖🔍** 