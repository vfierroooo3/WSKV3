import os
import hardwareDatabase
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv() 

# Get MongoDB server address from environment variable
MONGODB_SERVER = os.getenv("MONGODB_SERVER")

# Initial Hardware to be added to the database
INITIAL_HARDWARE = [
    {"hwName": "Jet", "capacity": 500},
    {"hwName": "Helicopter", "capacity": 800},
]

def seed(client):
    for hw in INITIAL_HARDWARE:
        result = hardwareDatabase.createHardwareSet(
            client,hw["hwName"],
            hw["capacity"]
        )
        print(result["message"],hw["hwName"])

if __name__ == "__main__":
    client = MongoClient(MONGODB_SERVER)
    seed(client)
    