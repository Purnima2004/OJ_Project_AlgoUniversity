# 🚀 Online Judge (OJ) - Competitive Programming Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://djangoproject.com)
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://docker.com)
[![AWS](https://img.shields.io/badge/AWS-EC2-orange.svg)](https://aws.amazon.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Live Demo:** [🌐 fullmoon.icu](https://fullmoon.icu) | **Status:** 🟢 Production Ready

A robust and scalable Online Judge web application built during a Software Development Externship. This platform enables users to solve competitive programming problems, participate in contests, and get AI-powered code feedback - all in a secure, sandboxed environment.

## ✨ Features

### 🎯 Core Functionality
- **Multi-Language Support**: Python, C++, Java with real-time compilation
- **Problem Management**: Create, edit, and manage programming problems with test cases
- **Contest System**: Real-time contests with timers and leaderboards
- **Code Execution**: Secure sandboxed code execution with Docker
- **AI Code Review**: Google Gemini AI integration for intelligent code analysis
- **Online Compiler**: Standalone compiler for testing code independently

### 🏆 Contest Features
- **Real-time Timer**: Countdown timers with visual warnings
- **Separate Contest Problems**: Unique problem sets for each contest
- **Leaderboard System**: Real-time ranking updates
- **Contest Management**: Admin tools for creating and managing contests
- **Anti-Cheating**: No AI review during contests for fair competition

### 🔐 Security & Performance
- **Docker Sandboxing**: Isolated code execution environment
- **User Authentication**: Secure login/registration system
- **Rate Limiting**: Protection against abuse
- **SSL/HTTPS**: Secure communication
- **Load Balancing**: Nginx reverse proxy for scalability

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.2+
- **Database**: SQLite (production-ready with PostgreSQL support)
- **Authentication**: Django built-in auth system
- **API**: RESTful endpoints with Django views

### Frontend
- **Markup**: HTML5 with semantic structure
- **Styling**: CSS3 with responsive design
- **JavaScript**: Vanilla JS for dynamic interactions
- **UI/UX**: Clean, intuitive interface optimized for coding

### Infrastructure
- **Containerization**: Docker with docker-compose
- **Cloud Platform**: AWS EC2 for scalable deployment
- **Web Server**: Nginx for reverse proxy and SSL termination
- **Process Manager**: Gunicorn for production WSGI server

### AI Integration
- **Model**: Google Gemini AI for code analysis
- **Features**: Code quality assessment, algorithm analysis, optimization suggestions
- **API**: Secure integration with environment variable configuration

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/oj-project.git
   cd oj-project
   ```

2. **Set up environment variables**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Add your Google Gemini API key
   echo "GEMINI_API_KEY=your_api_key_here" >> .env
   ```

3. **Run with Docker**
   ```bash
   cd oj_backend
   docker-compose up --build
   ```

4. **Access the application**
   - Main app: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

### Manual Setup

1. **Install dependencies**
   ```bash
   cd oj_backend
   pip install -r requirements.txt
   ```

2. **Run migrations**
   ```bash
   python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

4. **Start development server**
   ```bash
   python manage.py runserver
   ```

## 📁 Project Structure

```
oj_backend/
├── auth_app/                 # Main Django application
│   ├── templates/           # HTML templates
│   ├── static/             # CSS, JS, images
│   ├── views.py            # Main view logic
│   ├── models.py           # Database models
│   ├── compiler.py         # Code execution engine
│   ├── ai_review.py        # AI integration
│   └── oj_system.py        # Core OJ functionality
├── oj_backend/             # Django project settings
├── static/                 # Static files
├── media/                  # User uploads
├── db/                     # Database files
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Multi-container setup
├── nginx.conf             # Nginx configuration
└── requirements.txt        # Python dependencies
```

## 🌐 Deployment

### AWS EC2 Deployment

1. **Launch EC2 instance**
   ```bash
   # Use the provided deployment scripts
   ./deploy-aws.sh
   ```

2. **Configure environment**
   ```bash
   # Set production environment variables
   export IS_PRODUCTION=true
   export GEMINI_API_KEY=your_key
   ```

3. **Deploy with Docker**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

### Environment Variables

```bash
# Required
GEMINI_API_KEY=your_google_api_key
SECRET_KEY=your_django_secret_key

# Optional
DEBUG=False
IS_PRODUCTION=true
ALLOWED_HOSTS=your_domain.com
```

## 📊 Performance Metrics

- **Code Submission Latency**: < 5 seconds average
- **Supported Languages**: 3 (Python, C++, Java)
- **Concurrent Users**: Scalable architecture
- **Test Case Coverage**: Comprehensive evaluation system
- **Uptime**: Production-grade reliability

## 🔧 Configuration

### AI Review Setup

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set environment variable: `GEMINI_API_KEY=your_key`
3. AI review will be available in problem-solving interface

### Contest Management

- Create contests through admin panel
- Set custom time limits and problem sets
- Monitor participant progress in real-time
- Automatic contest ending with timer

### Problem Creation

- Rich text editor for problem descriptions
- Multiple test case support
- Difficulty level classification
- Sample input/output examples

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Mentorship**: Senior engineers from Google London, Apple, and Alphagrep Singapore
- **Technologies**: Django, Docker, AWS, Google Gemini AI
- **Community**: Open source contributors and competitive programming community

## 📞 Contact

- **Project Link**: [https://github.com/yourusername/oj-project](https://github.com/Purnima2004/OJ_Project_AlgoUniversity)
- **Live Demo**: [https://fullmoon.icu](https://fullmoon.icu)
- **Issues**: [GitHub Issues](https://github.com/Purnima2004/OJ_Project_AlgoUniversity/issues)

---

⭐ **Star this repository if you find it helpful!**

---

*Built with ❤️ during Software Development Externship*
