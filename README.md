# AI Powered Medical Sentiment Analysis

This project is an AI-powered web application for analyzing the sentiment of medical claims and extracting named entities (NER) from user input. It features a Flask REST API backend with MongoDB for storage, a machine learning model for sentiment analysis, and a modern HTML/JS frontend dashboard.

## 🚀 Features

- **Medical Sentiment Analysis**: Predicts sentiment (positive/negative/neutral) from medical claim text
- **Named Entity Recognition (NER)**: Extracts entities like drugs, organizations, dates, etc.
- **MongoDB Integration**: Stores analysis results and user data
- **Modern Dashboard**: Responsive frontend with dark mode, PDF export, and user settings
- **RESTful API**: Flask-based API for easy integration
- **Dockerized**: Easily deployable with Docker and Docker Compose
- **Real-time Analysis**: Instant sentiment prediction and entity extraction

## 📁 Folder Structure

```
AI_powered_Medical_sentiment_analysis/
│
├── Backend/
│   └── routes/
│       ├── routes.py              # Flask API routes
│       └── Dockerfile             # Backend containerization
│
├── config/
│   └── database/
│       └── config.py              # Database configuration
│
├── frontend/
│   └── User_interface/
│       ├── Medical_Analysis.html  # Main frontend interface
│       ├── script.js              # JavaScript functionality
│       └── style.css              # Styling and themes
│   └── Dashboard/
│       └── dashboard.py           # Dashboard backend logic
│
├── notebooks/
│   ├── logistic_regression.pkl    # Trained sentiment model
│   └── Vectorize.pkl             # Text vectorization model
│
├── test/
│   └── Server_test.json          # API testing configuration
│
├── logs/                         # Application logs
│
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
├── docker-compose.yaml           # Docker orchestration
├── README.md                     # Project documentation
└── LICENSE                       # Project license
```

## 🔧 Quick Start

### Prerequisites

- Python 3.8+
- Docker & Docker Compose (optional)
- MongoDB (local or cloud instance)

### 1. Clone the Repository

```bash
git clone https://github.com/Shivansh-datascience/Medical_Claim_sentiment_analysis.git
cd Medical_Claim_sentiment_analysis
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
MONGO_DB_URL=mongodb://localhost:27017
MONGO_DB_DATABASE=medical_sentiment_db
MONGO_DB_COLLECTION=sentiment_analysis

# Flask Configuration
FLASK_SECRET_KEY=your-very-secret-key-here
FLASK_DEBUG=True

# API Configuration
API_HOST=127.0.0.1
API_PORT=5000
```

### 3. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 4. Run the Application

#### Option A: Direct Python Execution
```bash
# Start the Flask API
cd Backend/routes
python routes.py
```

#### Option B: Docker Compose (Recommended)
```bash
# Build and run all services
docker-compose up --build
```

## 🌐 API Endpoints

### Core Endpoints

| Endpoint | Method | Description | URL |
|----------|--------|-------------|-----|
| Sentiment Analysis | POST | Analyze medical text sentiment | `http://127.0.0.1:5000/Predict_Sentiment` |
| Server Status | GET | Check server health | `http://127.0.0.1:5000/Check_Server_status` |
| Production API | POST | Production-ready endpoint | `http://0.0.0.0:5000/Predict_Sentiment` |

### Request Format

```json
{
    "text": "Patient shows improvement after medication",
    "user_id": "user123",
    "claim_id": "claim456"
}
```

### Response Format

```json
{
    "sentiment": "positive",
    "confidence": 0.87,
    "entities": [
        {
            "text": "medication",
            "label": "TREATMENT",
            "start": 35,
            "end": 45
        }
    ],
    "timestamp": "2024-01-15T10:30:00Z",
    "status": "success"
}
```

## 🧪 Testing

### API Testing with Postman

1. Import the test configuration from `test/Server_test.json`
2. Send POST request to sentiment analysis endpoint
3. Include medical text in request body

<img width="1920" height="1080" alt="Screenshot (74)" src="https://github.com/user-attachments/assets/494beef0-114b-4a66-a006-bebba89ed11e" />


### Example Test Cases

```bash
# Test positive sentiment
curl -X POST http://127.0.0.1:5000/Predict_Sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "Patient recovered well after treatment"}'

# Test server status
curl -X GET http://127.0.0.1:5000/Check_Server_status
```

## 🎨 Frontend Usage

### Accessing the Interface

1. **Local Development**: Open `frontend/User_interface/Medical_Analysis.html` in your browser
2. **Served Application**: Navigate to `http://127.0.0.1:5000` (if serving via Flask)

### Features

- **Dark/Light Mode**: Toggle between themes
- **Real-time Analysis**: Instant sentiment prediction
- **Entity Highlighting**: Visual NER results
- **Export Options**: PDF reports and data export
- **History Tracking**: Previous analyses storage

## 🗄️ Database Schema

### MongoDB Collections

#### `sentiment_analysis` Collection
```json
{
    "_id": "ObjectId",
    "user_id": "string",
    "claim_id": "string",
    "text": "string",
    "sentiment": "positive|negative|neutral",
    "confidence": "number",
    "entities": "array",
    "timestamp": "datetime",
    "session_id": "string"
}
```



## 🔐 Environment Configuration

### Required Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGO_DB_URL` | MongoDB connection string | `mongodb://localhost:27017` | Yes |
| `MONGO_DB_DATABASE` | Database name | `medical_sentiment_db` | Yes |
| `MONGO_DB_COLLECTION` | Collection name | `sentiment_analysis` | Yes |
| `FLASK_SECRET_KEY` | Flask session key | - | Yes |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_DEBUG` | Debug mode | `False` |
| `API_HOST` | API host | `127.0.0.1` |
| `API_PORT` | API port | `5000` |

## 📊 Model Information

### Sentiment Analysis Model
- **Algorithm**: Logistic Regression
- **Features**: TF-IDF Vectorization
- **Training Data**: Medical claims dataset
- **Performance**: ~87% accuracy on test set

### Named Entity Recognition
- **Model**: spaCy NLP pipeline
- **Entities**: PERSON, ORG, DATE, TREATMENT, CONDITION
- **Language**: English medical text

## 🛠️ Development

### Project Setup
```bash
# Clone and setup
git clone <repository-url>
cd Medical_Claim_sentiment_analysis

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Format code
black . --line-length 88
flake8 .
```

### Adding New Features

1. **Backend**: Add routes in `Backend/routes/routes.py`
2. **Frontend**: Modify `frontend/User_interface/` files
3. **Database**: Update `config/database/config.py`
4. **Models**: Add new models in `notebooks/` directory

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| MongoDB Connection Error | Check `MONGO_DB_URL` in `.env` file |
| Model Loading Error | Ensure `.pkl` files exist in `notebooks/` |
| CORS Issues | Verify frontend URL in Flask-CORS config |
| Port Already in Use | Change `API_PORT` in `.env` or kill process |

### Debug Mode

```bash
# Enable debug logging
export FLASK_DEBUG=1
export FLASK_ENV=development

# Run with verbose logging
python routes.py --verbose
```

## 📈 Performance Monitoring

### Logging

- **Location**: `logs/` directory
- **Levels**: DEBUG, INFO, WARNING, ERROR
- **Format**: JSON structured logging

### Metrics

- API response times
- Model prediction accuracy
- Database query performance
- User interaction analytics

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Shivansh** - *Initial work* - [Shivansh-datascience](https://github.com/Shivansh-datascience)

## 🙏 Acknowledgments

- Medical NLP research community
- Flask and MongoDB documentation
- Open source ML libraries (scikit-learn, spaCy)
- Frontend design inspiration from modern dashboards

## 📞 Support

For support and questions:

- **Email**: shivanshbajpai2011@gmail.com
- **Issues**: [GitHub Issues](https://github.com/Shivansh-datascience/Medical_Claim_sentiment_analysis/issues)
- **Documentation**: [Project Wiki](https://github.com/Shivansh-datascience/Medical_Claim_sentiment_analysis/wiki)

---

⭐ If you find this project helpful, please give it a star on GitHub!

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced NER for medical entities
- [ ] Real-time dashboard analytics
- [ ] Mobile application
- [ ] Integration with EHR systems
- [ ] Advanced visualization charts
- [ ] User authentication system
- [ ] API rate limiting
- [ ] Automated model retraining
- [ ] Cloud deployment templates

