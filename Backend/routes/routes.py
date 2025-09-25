import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS 
from pymongo import MongoClient
from pydantic import BaseModel
import os
import json
import spacy
import requests
import joblib
import logging
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Setup logging
# -----------------------------
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# -----------------------------
# Initialize Flask app
# -----------------------------
app = Flask(__name__)
CORS(app, origins=["*"])  # Allow frontend to access backend APIs

SERVER_NAME = '127.0.0.1'  # Localhost
SERVER_PORT = 5000          # Flask port

# -----------------------------
# MongoDB Setup
# -----------------------------
class Mongodb_credentials(BaseModel):
    """Pydantic model to validate MongoDB credentials"""
    mongodb_client_url: str

def Authenticate_mongodb_credentials(mongodb_client_url):
    """Authenticate and connect to MongoDB"""
    try:
        mongo_authentication_client = MongoClient(mongodb_client_url)
        return mongo_authentication_client
    except Exception as connection_error:
        logger.error(connection_error)
        return None

# Connect to MongoDB using credentials from environment variables
mongo_client = Authenticate_mongodb_credentials(os.getenv("Mongo_db_url"))

if mongo_client:
    print("Connected to Mongo client")
    mongo_db = mongo_client[os.getenv("Mongo_db_database")]
    mongo_collections = mongo_db[os.getenv("Mongo_db_collection")]

    if mongo_db is not None:
        print("Connected to Mongo database with collections")
    else:
        print('Error in connecting to Mongo Database with collections')
else:
    print("Error in connecting to Mongo client")

# -----------------------------
# Load Machine Learning Models
# -----------------------------
file_path_lr = r"D:\AI_powered_Medical_sentiment_analysis\notebooks\logistic_regression.pkl"
file_path_vectors = r"D:\AI_powered_Medical_sentiment_analysis\notebooks\Vectorize.pkl"

# Load logistic regression model and vectorizer
lr_model = joblib.load(file_path_lr)
vectors = joblib.load(file_path_vectors)

# -----------------------------
# Load Spacy NER Model
# -----------------------------
def load_spacy_model(model_name: str):
    """Load a pre-trained Spacy NER model"""
    logger.info("Loading Spacy Pretrained model from environment")
    spacy_model = spacy.load(model_name)  
    return spacy_model

# -----------------------------
# Keyword-based positive sentiment detection
# -----------------------------
POSITIVE_KEYWORDS = ["good", "excellent", "improved", "beneficial", "successful", "happy", "recovered"]

def keyword_sentiment_analysis(text: str) -> str:
    """
    Check if any positive keywords are present in the text.
    Returns 'positive' if any keyword is found, otherwise 'neutral_or_negative'.
    """
    text_lower = text.lower()
    for word in POSITIVE_KEYWORDS:
        if word in text_lower:
            return "positive"
    return "neutral_or_negative"

# -----------------------------
# Route: Predict Sentiment
# -----------------------------
@app.route("/Predict_Sentiment", methods=['POST'])
def predict_sentiment():
    """
    Hybrid sentiment:
    - Positive text (keyword detected) → returns positive with model-based probability
    - Neutral/Negative → returns LR prediction and probability
    Also includes NER results.
    """
    try:
        claim_json = request.get_json(force=True)

        if 'Medical_Claim' not in claim_json:
            return jsonify({"error": "Missing Medical Claims Request"}), 400

        claim_text = claim_json['Medical_Claim']

        # Load Spacy model once per request
        spacy_model = load_spacy_model("en_core_web_sm")
        spacy_model_doc = spacy_model(claim_text)
        ner_results = [{"text": ent.text, "label": ent.label_} for ent in spacy_model_doc.ents]

        results_list = []

        # Check for positive keywords
        keyword_sentiment = keyword_sentiment_analysis(claim_text)

        # Vectorize text
        claim_text_array = np.array([claim_text])
        vectors_text = vectors.transform(claim_text_array)
        lr_model_pred_proba = lr_model.predict_proba(vectors_text)[0]

        if keyword_sentiment == "positive":
            # Get probability of positive class dynamically
            if "positive" in lr_model.classes_:
                positive_class_index = list(lr_model.classes_).index("positive")
            else:
                positive_class_index = np.argmax(lr_model_pred_proba)
            positive_score = float(lr_model_pred_proba[positive_class_index])

            positive_result = {
                'Sentiment_Text': claim_text,
                'Sentiment_Prediction': "positive",
                'Sentiment_Score': round(positive_score, 2),
                'NER_Results': ner_results
            }
            results_list.append(positive_result)
        else:
            # Neutral or negative prediction
            lr_model_pred = lr_model.predict(vectors_text)[0]
            max_proba = float(np.max(lr_model_pred_proba))
            lr_result = {
                'Sentiment_Text': claim_text,
                'Sentiment_Prediction': lr_model_pred,
                'Sentiment_Score': round(max_proba, 3),
                'NER_Results': ner_results
            }
            results_list.append(lr_result)

        # Store in MongoDB
        try:
            for res in results_list:
                insert_result = mongo_collections.insert_one(res)
                res["_id"] = str(insert_result.inserted_id)
        except Exception as db_err:
            logger.error(f"MongoDB Insert Error: {db_err}")

        return jsonify(results_list)

    except Exception as e:
        return jsonify({'Exception Occurred': str(e)})

# -----------------------------
# Route: Check Server Status
# -----------------------------
@app.route("/Check_Server_status", methods=['GET'])
def check_server_running_process():
    server_address = f"http://{SERVER_NAME}:{SERVER_PORT}/Predict_Sentiment"
    file_location = r"D:\AI_powered_Medical_sentiment_analysis\test\Server_test.json"

    try:
        server_response = requests.post(server_address, json={"Medical_Claim": "Test claim for health check."})

        status_message = {
            "Server_Running_Address": server_address,
            "Server_host": SERVER_NAME,
            "Server_port": SERVER_PORT,
            "Server_Status": "Success" if server_response.status_code == 200 else "Failed",
            "Server_status_code": server_response.status_code
        }

        with open(file_location, 'w') as file:
            json.dump(status_message, file)

        return jsonify(status_message)

    except Exception as e:
        return jsonify({"Exception Occurred": str(e)})

# -----------------------------
# Run Flask App
# -----------------------------
if __name__ == '__main__':
    app.secret_key = np.random.bytes(24)  # Generate random secret key for session security
    app.run(host=SERVER_NAME, port=SERVER_PORT, debug=True)
