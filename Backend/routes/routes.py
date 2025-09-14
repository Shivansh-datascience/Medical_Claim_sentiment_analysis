import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS 
from bson import ObjectId
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.asynchronous.client_session import AsyncClientSession
from pydantic import BaseModel
import os
import json
import spacy
import requests
import joblib
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app,origins=["*"])   #using CORS Policy to act as bridge between frontend and backend 

SERVER_NAME = '127.0.0.1'   #local host server address
SERVER_PORT = 5000   #local host port number 

#validate the Mongo client connection using Pydantic 
class Mongodb_credentials(BaseModel):
    mongodb_client_url: str

def Authenticate_mongodb_credentials(mongodb_client_url):
    try:
        mongo_authentication_client = MongoClient(mongodb_client_url)
        return mongo_authentication_client
    except Exception as connection_error:
        logger.error(connection_error)
        return None

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

file_path_lr = r"D:\AI_powered_Medical_sentiment_analysis\notebooks\logistic_regression.pkl"
file_path_vectors = r"D:\AI_powered_Medical_sentiment_analysis\notebooks\Vectorize.pkl"

lr_model = joblib.load(file_path_lr)
vectors = joblib.load(file_path_vectors)

#create function to load pre trained NER model
def load_spacy_model(model_name : str)->spacy:

    #create event session for load process
    logger.info("Loading Spacy Pretrained model from environment")
    spacy_model = spacy.load(model_name)  
    if spacy_model is not None:
        return spacy_model  #return model object
    else:
        return f"Unable to  Pull Model {model_name} from Pretrained Environment"

#create route directory to return the sentiments score
@app.route("/Predict_Sentiment", methods=['POST'])
def predict_sentiment():

    """ Create Exception Handling for Analyse Sentiment Behaviour"""
    try:
        claim_json = request.get_json(force=True)  #access json request

        #validate the user  json input 
        if 'Medical_Claim' not in claim_json:
            return jsonify(
                {
                    "error":"Missing Medical Claims Request "
                }
            ),400   #return the status response as 400

        claim_text = claim_json['Medical_Claim']   #access the text claim from json key

        claim_text_array = np.array([claim_text])  #convert into nupy array

        vectors_text = vectors.transform(claim_text_array)  #convert into vectors 
        
        lr_model_pred = lr_model.predict(vectors_text)  #predict the sentiment behaviour

        lr_model_pred_proba = lr_model.predict_proba(vectors_text)  #predict the sentiment score

        #access the max probability
        max_proba = float(np.max(lr_model_pred_proba[0]))

        #load model function
        model_name = "en_core_web_sm"
        spacy_model = load_spacy_model(model_name)  #call function for load model
        spacy_model_doc = spacy_model(claim_text)


        #iterate through all entities 
        ner_results = [{"text": ent.text, "label": ent.label_} for ent in spacy_model_doc.ents]

        if lr_model_pred is not None:
            #return the result in json format 
            result = {
                'Sentiment_Text':claim_text,
            'Sentiment_Prediction': lr_model_pred[0],
            'Sentiment_Score': max_proba,  # maximum probability
            'NER_Results': ner_results     # return all entities
            }
            # store in MongoDB Database 
            try:
                insert_result = mongo_collections.insert_one(result)
                # Add the inserted ObjectId as a string to the response
                result["_id"] = str(insert_result.inserted_id)
            except Exception as db_err:
                logger.error(f"MongoDB Insert Error: {db_err}")
            
            #return json message 
            return jsonify(result)  
        else:
            return jsonify(
        {
            'Unable To Analyse the Sentiment For Users Claim': None
        }
        )

        
    except Exception as e:
        return jsonify(
            {
                'Exception Occurred': str(e)
            }
        )


#create route directory to check servers status with HTTP protocol
@app.route("/Check_Server_status", methods=['GET'])
def check_server_running_process():
    server_address = f"http://{SERVER_NAME}:{SERVER_PORT}/Predict_Sentiment"
    file_location = r"D:\AI_powered_Medical_sentiment_analysis\test\Server_test.json"

    try:
        # ✅ Correct HTTP method and payload
        server_response = requests.post(server_address, json={"Medical_Claim": "Test claim for health check."})

        if server_response.status_code == 200:
            success_message = {
                "Server_Running_Address": server_address,
                "Server_host": SERVER_NAME,
                "Server_port": SERVER_PORT,
                "Server_Status": "Success",
                "Server_status_code": server_response.status_code
            }

            with open(file_location, 'w') as file:
                json.dump(success_message, file)

            return jsonify(success_message)
        else:
            fail_message = {
                "Server_Address": server_address,
                "Server_Host": SERVER_NAME,
                "Server_port": SERVER_PORT,
                "Server_Status": "Failed",
                "Server_status_code": server_response.status_code
            }

            with open(file_location, 'w') as file:
                json.dump(fail_message, file)

            return jsonify(fail_message)

    except Exception as e:
        return jsonify({"Exception Occurred": str(e)})
#call the main function to run flask application
if __name__ == '__main__':

    #authenticate flask cookies session with secret key identification

    cookies_secret_key = np.random.bytes(24)  #generate 24 bytes long key

    app.secret_key = cookies_secret_key  #add random number to secret key

    app.run(
        host=SERVER_NAME,port=SERVER_PORT,debug=True)
    


    
    
