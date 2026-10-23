import os
from pymongo import MongoClient

client = MongoClient(
    os.environ["MONGODB_URI"],
    serverSelectionTimeoutMS=5000
)

db = client["project_db"]