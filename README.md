# AI Powered Medical Sentiment Analysis

This project is an AI-powered web application for analyzing the sentiment of medical claims and extracting named entities (NER) from user input. It features a Flask REST API backend with MongoDB for storage, a machine learning model for sentiment analysis, and a modern HTML/JS frontend dashboard.

## Features

- **Medical Sentiment Analysis**: Predicts sentiment (positive/negative/neutral) from medical claim text.
- **Named Entity Recognition (NER)**: Extracts entities like drugs, organizations, dates, etc.
- **MongoDB Integration**: Stores analysis results and user data.
- **Modern Dashboard**: Responsive frontend with dark mode, PDF export, and user settings.
- **Dockerized**: Easily deployable with Docker and Docker Compose.

## Folder Structure

```
AI_powered_Medical_sentiment_analysis/
│
├── Backend/
│   └── routes/
│       ├── routes.py
│       ├── Dockerfile
│
├── config/
│   └── database/
│       └── config.py
│
├── frontend/
│   └── User_interface/
│       ├── Medical_Analysis.html
│
├── notebooks/
│   ├── logistic_regression.pkl
│   ├── Vectorize.pkl
│
├── test/
│   └── Server_test.json
│
├── logs/
│
├── .env
├── requirements.txt
├── docker-compose.yaml
├── README.md
└── LICENSE
```

## Quick Start

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/AI_powered_Medical_sentiment_analysis.git
cd AI_powered_Medical_sentiment_analysis
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```
Mongo_db_url=mongodb://mongo:27017
Mongo_db_database=medical_sentiment_db
Mongo_db_collection=sentiment_analysis
FLASK_SECRET_KEY=your-very-secret-key
```

### 3. Build and Run with Docker Compose

```sh
docker-compose up --build
```

- The API will be available at [http://localhost:5000](http://localhost:5000)
- The frontend can be opened by opening `frontend/User_interface/Medical_Analysis.html` in your browser.

### 4. Test the API

You can use Postman or curl:

```sh
curl -X POST http://localhost:5000/Predict_Sentiment \
     -H "Content-Type: application/json" \
     -d '{"Medical_Claim": "Patient is feeling much better after medication."}'
```

## Customization

- Update the ML models in `notebooks/` as needed.
- Adjust frontend API URLs if deploying to a different host/port.

