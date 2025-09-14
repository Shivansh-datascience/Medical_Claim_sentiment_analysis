import pymongo 
from pymongo import MongoClient
from pymongo.auth import authenticate
import os
import logging
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

#setup the basic configuration of loging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

""" Configure the Database authentication """
try:

    #create an event for tracking the status
    logger.info("Fetching Mongo database credentials ")

    #fetch mongo Database client side URL path from environmemnt
    logger.info("Fetch Mongo Database client side url path")
    mongo_db_client_url = os.getenv("Mongo_db_url")  #define key wrt to environment variables

    logger.info("Fetch Mongo Database Name")
    #fetch mongo Database client side database details
    mongo_db_database = os.getenv("Mongo_db_database")

    #fetch mongo Database client side database collections
    logger.info("Fetch Mongo database collection name")
    mongo_db_collection = os.getenv("Mongo_db_collection")

     #fetch mongo Database client side database collections
    logger.info("Fetch Mongo database running port ")
    mongo_db_port = os.getenv("Mongo_db_port")
    
    
    #define an iterable list containing all database credentials 
    database_credentials = [
        mongo_db_database ,mongo_db_client_url , 
        mongo_db_collection , mongo_db_port
    ]
    if any(database_credentials) == None:
        print("Database credettials not fetched ! Load Environment variable")

    elif all(database_credentials) != None:
        print("fetched Database credentials from Environment Variables")
except Exception as e:
    logger.error(e)


