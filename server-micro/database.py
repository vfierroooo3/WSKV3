import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(
    os.environ["MONGODB_URI"],
    serverSelectionTimeoutMS=5000
)

db = client["project_db"]