import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv() 

# Get MongoDB server address from environment variable
MONGODB_SERVER = os.getenv("MONGODB_SERVER")

# Connect to MongoDB
client = MongoClient(MONGODB_SERVER)

def access_collection(collection_name):
    '''Enter Collection Name to Access From Database'''
    db = client.WSKV3
    return db[collection_name]
