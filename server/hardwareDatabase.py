# Import necessary libraries and modules
from pymongo import MongoClient

'''
Structure of Hardware Set entry:
HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
}
'''

# Function to create a new hardware set
def createHardwareSet(client, hwSetName, initCapacity):
    # Create a new hardware set in the database
        db = client.WSKV3
        collection = db.HardwareSets

        hardwareSet = {
             "hwName": hwSetName,
             "capacity":initCapacity,
             "availability":initCapacity
        }

        result = collection.insert_one(hardwareSet)
        return result.inserted_id

    

# Function to query a hardware set by its name
def queryHardwareSet(client, hwSetName):
    # Query and return a hardware set from the database
    db = client.WSKV3
    collection = db.HardwareSets
    return collection.find_one({"hwName": hwSetName})

# Function to update the availability of a hardware set
def updateAvailability(client, hwSetName, newAvailability):
    # Update the availability of an existing hardware set
    db = client.WSKV3
    collection = db.HardwareSets
    result = collection.update_one(
         {"hwName": hwSetName},
         {"$set": {"availability": newAvailability}}
    )
    return result.modified_count > 0  # Return True if the update was successful, False otherwise

# Function to request space from a hardware set
def requestSpace(client, hwSetName, amount):
    # Request a certain amount of hardware and update availability
    db = client.WSKV3
    collection = db.HardwareSets
    hardware_set = collection.find_one({"hwName": hwSetName})
    return hardware_set and hardware_set['availability'] >= amount

# Function to get all hardware set names
def getAllHwNames(client):
    # Get and return a list of all hardware set names
    db = client.WSKV3
    collection = db.HardwareSets
    return [hw['hwName'] for hw in collection.find({}, {"_id": 0, "hwName": 1})]

