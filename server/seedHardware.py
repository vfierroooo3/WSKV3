from pymongo import MongoClient
import databaseHelpers
import hardwareDatabase

# Initial Hardware to be added to the database
INITIAL_HARDWARE = [
    {"hwName": "Jet", "capacity": 500},
    {"hwName": "Helicopter", "capacity": 800},
]


def seed(client):
    for hw in INITIAL_HARDWARE:
        result = hardwareDatabase.createHardwareSet(client,hw["hwName"],hw["capacity"])
        print(result["message"],hw["hwName"])

if __name__ == "__main__":
    client = MongoClient("mongodb+srv://katierafdahl_db_user:45sfmVPrbATWYm3t@wskv3.zcpyq8u.mongodb.net/?appName=WSKV3")
    seed(client)
    