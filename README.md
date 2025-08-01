# 🚀 Hacksky - Instagram Clone with AI Misinformation Detection

A modern Instagram-like social media platform with integrated AI-powered misinformation detection. Built with HTML/CSS/JavaScript frontend and Python FastAPI backend.

![Hacksky Demo](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 📱 **Frontend - Instagram Clone**
- **Modern UI/UX**: Instagram-inspired design with responsive layout
- **Dynamic Feed**: Real-time posts with infinite scroll
- **Stories System**: Interactive story circles with viewing states
- **User Management**: Profile switching and customization
- **Content Creation**: Drag & drop image upload with preview
- **Interactive Features**: Like, save, share, and comment functionality
- **Search & Discovery**: Real-time search and user suggestions
- **Mobile Responsive**: Optimized for all device sizes

### 🤖 **Backend - AI Misinformation Detection**
- **Real AI Analysis**: Hugging Face models for content classification
- **Multi-modal Detection**: Text, image, audio, and video analysis
- **Trust Scoring**: 0-100% confidence scores with detailed reasoning
- **Cross-modal Consistency**: Detects inconsistencies between text and media
- **Real-time Processing**: Instant analysis of user-generated content
- **Comprehensive Logging**: Detailed detection logs and system monitoring
- **RESTful API**: FastAPI endpoints for frontend integration

### 🔍 **Misinformation Detection Capabilities**
- **Text Analysis**: Detects misleading claims, conspiracy theories, and fake news
- **Content Classification**: Categorizes content as credible, misinformation, satire, or clickbait
- **Trust Scoring**: Provides confidence levels with explainable AI reasoning
- **Real-time Alerts**: Visual indicators for potentially misleading content
- **Cross-modal Verification**: Ensures consistency between text and media content

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Modern web browser
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hacksky.git
   cd hacksky
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Start the application (Recommended)**
   ```bash
   python start.py
   ```
   This will start both backend and frontend servers automatically.

   **Or start manually:**
   ```bash
   # Start backend
   cd backend
   python run.py
   
   # Start frontend (in new terminal)
   cd frontend
   python -m http.server 8080
   ```

4. **Access the application**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

5. **Test the system**
   - Create posts with various content types
   - Watch the terminal for real-time AI analysis
   - Observe trust scores and misinformation alerts

## 🏗️ Project Structure

```
hacksky/
├── 📁 Frontend Files
│   ├── index.html              # Main HTML structure
│   ├── styles.css              # Complete styling and animations
│   ├── script.js               # Frontend functionality and API integration
│   └── morgan.mp4              # Sample video content
│
├── 📁 Backend System
│   ├── main.py                 # FastAPI application entry point
│   ├── agent.py                # Autonomous AI agent
│   ├── config.py               # Configuration management
│   ├── requirements.txt        # Python dependencies
│   ├── run.py                  # Server startup script
│   └── test_backend.py         # Comprehensive test suite
│
├── 📁 Detection Engine
│   ├── detection/
│   │   ├── pipeline.py         # Main detection pipeline
│   │   ├── huggingface_detector.py  # Real AI model integration
│   │   └── cross_modal_detector.py  # Multi-modal analysis
│   ├── feed/
│   │   └── fake_feed.py        # Content generation for testing
│   └── logs/
│       └── logger.py           # Logging and monitoring system
│
├── 📄 Documentation
│   ├── README.md               # This file
│   ├── HUGGINGFACE_SETUP.md    # AI model setup guide
│   ├── LICENSE                 # MIT License
│   └── install_huggingface.bat # Windows setup script
│
└── 🧪 Testing
    └── test_huggingface_integration.py  # AI integration tests
```

## 🔧 Configuration

### Backend Configuration
Edit `backend/config.py` or create a `.env` file:

```python
# Debug Configuration
DEBUG: bool = True

# API Configuration
API_HOST: str = "0.0.0.0"
API_PORT: int = 8000

# Detection Settings
MIN_TRUST_SCORE: float = 0.5
MAX_TRUST_SCORE: float = 1.0
```

### Environment Variables
Create a `.env` file in the backend directory:
```env
DEBUG=false
API_HOST=127.0.0.1
API_PORT=8080
AGENT_LOOP_INTERVAL=5.0
```

## 📡 API Endpoints

### Base URL: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and status |
| `/analyze` | POST | Analyze content for misinformation |
| `/detect-cross-modal` | POST | Multi-modal content analysis |
| `/status` | GET | Agent and system health |
| `/logs` | GET | Recent detection logs |
| `/logs/low-trust` | GET | Low trust score logs |
| `/docs` | GET | Interactive API documentation |

### Example API Usage

```bash
# Analyze text content
curl -X POST "http://localhost:8000/analyze" \
  -F "content=This is a test message" \
  -F "content_type=text"

# Get system status
curl http://localhost:8000/status

# View recent logs
curl http://localhost:8000/logs
```

## 🤖 AI Detection Features

### Content Analysis
- **Text Classification**: Uses Hugging Face models to classify content
- **Trust Scoring**: 0-100% confidence scores with detailed reasoning
- **Multi-modal Detection**: Analyzes text, images, audio, and video
- **Cross-modal Consistency**: Ensures content consistency across media types

### Detection Categories
- ✅ **Credible Information**: Factual, well-sourced content
- 🚨 **Misinformation**: False or misleading claims
- 🎭 **Satire**: Humorous or satirical content
- 📢 **Clickbait**: Sensationalist headlines
- 🔍 **Conspiracy Theory**: Unsubstantiated conspiracy claims
- 📰 **Factual News**: Verified news content

### Example Detection Output
```
📊 Analysis Result for Post #1:
   Trust Score: 15/100 🚨
   Reason: AI model classified as conspiracy theory with 87.3% confidence. 
           Claims appear to be unsubstantiated.
   Classification: conspiracy_theory
   Confidence: 87.3%
```

## 🎨 Frontend Features

### User Interface
- **Instagram-like Design**: Familiar, intuitive interface
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Smooth Animations**: Heart beats, fade-ins, and transitions
- **Modern Components**: Modals, notifications, and interactive elements

### Interactive Features
- **Post Creation**: Upload images with captions
- **Social Interactions**: Like, save, share, and comment
- **User Profiles**: Customizable profiles with bio and avatar
- **Search Functionality**: Find users and content
- **Story System**: View and create stories
- **Real-time Updates**: Live feed updates and notifications

### Content Management
- **Infinite Scroll**: Continuous content loading
- **Image Upload**: Drag & drop with preview
- **Caption Writing**: Rich text with emoji support
- **Content Moderation**: AI-powered content analysis
- **Trust Indicators**: Visual alerts for content credibility

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
python test_backend.py
```

### Test AI Integration
```bash
python test_huggingface_integration.py
```

### Frontend Testing
- Open browser developer tools
- Test all interactive features
- Verify responsive design
- Check API integration

## 🚨 Troubleshooting

### Common Issues

**Backend Won't Start:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Install dependencies
pip install -r requirements.txt

# Check port availability
netstat -an | grep 8000
```

**AI Models Not Loading:**
```bash
# Install AI dependencies
pip install transformers torch accelerate

# Check internet connection for model download
python test_huggingface_integration.py
```

**Frontend Not Connecting:**
- Ensure backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify API endpoints are accessible

### Debug Mode
Set `DEBUG=True` in `backend/config.py` for:
- Detailed console logging
- Auto-reload on file changes
- Extended error messages
- Real-time system monitoring

## 🔮 Future Enhancements

### Planned Features
- **Real-time Messaging**: Direct message system
- **Advanced Analytics**: Detection trends and patterns
- **User Authentication**: Login and registration system
- **Database Integration**: Persistent data storage
- **Content Sources**: Real social media API integration
- **Advanced AI Models**: More sophisticated detection algorithms

### AI Model Improvements
- **Multi-language Support**: Detection in multiple languages
- **Deepfake Detection**: Advanced video and image analysis
- **Sentiment Analysis**: Emotional content classification
- **Fact-checking Integration**: Real-time fact verification
- **Explainable AI**: Detailed reasoning for all detections

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   cd backend && python test_backend.py
   ```
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Ensure mobile responsiveness

## 📊 Performance

### Current Metrics
- **Posts per second**: ~0.5 (configurable)
- **Memory usage**: ~50MB (backend)
- **API response time**: <100ms
- **AI analysis time**: 1-3 seconds
- **Uptime**: Continuous operation

### Optimization Opportunities
- Async processing for multiple posts
- Caching for repeated analysis
- Database indexing for log queries
- Model optimization and quantization
- CDN for static assets

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Instagram** for design inspiration
- **Hugging Face** for AI models and transformers
- **Unsplash** for beautiful stock images
- **Font Awesome** for the icon library
- **FastAPI** for the excellent web framework
- **OpenAI Whisper** for audio analysis capabilities

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/hacksky/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/hacksky/discussions)
- **Email**: your.email@example.com

---

**Ready to explore the future of social media with AI-powered content moderation! 🚀🤖**

*Built with ❤️ for a safer, more trustworthy online experience.*