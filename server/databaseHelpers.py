from pymongo import MongoClient

# Define the MongoDB connection string
MONGODB_SERVER = "mongodb+srv://katierafdahl_db_user:45sfmVPrbATWYm3t@wskv3.zcpyq8u.mongodb.net/?appName=WSKV3"
# Connect to MongoDB
client = MongoClient(MONGODB_SERVER)

def access_collection(collection_name):
    '''Enter Collection Name to Access From Database'''
    db = client.WSKV3
    return db[collection_name]
