import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

load_dotenv(Path(__file__).with_name(".env"))

client = MongoClient(
    os.environ["MONGODB_URI"],
    serverSelectionTimeoutMS=5000
)

# Project DB
project_db = client["apad-projects"]

# Hardware DB
hardware_db = client["apad-hardware"]