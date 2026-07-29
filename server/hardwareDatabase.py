# Import necessary libraries and modules
from pymongo import MongoClient
import databaseHelpers

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
        
        collection = databaseHelpers.access_collection(client, "HardwareSets")

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
    collection = databaseHelpers.access_collection(client, "HardwareSets")
    return collection.find_one({"hwName": hwSetName})

# Function to update the availability of a hardware set
def updateAvailability(client, hwSetName, newAvailability):
    # Update the availability of an existing hardware set
    collection = databaseHelpers.access_collection(client, "HardwareSets")
    result = collection.update_one(
         {"hwName": hwSetName},
         {"$set": {"availability": newAvailability}}
    )
    return result.modified_count > 0  # Return True if the update was successful, False otherwise

# Function to request space from a hardware set
def requestSpace(client, hwSetName, amount):
    # Request a certain amount of hardware and update availability
    collection = databaseHelpers.access_collection(client, "HardwareSets")
    hardware_set = collection.find_one({"hwName": hwSetName})
    if not hardware_set or hardware_set ['availability'] < amount:
         return False # Not enough availability or hardware set does not exist
    result = collection.update_one(
         {"hwName": hwSetName},
         {"$inc": {"availability": -amount}}
    )
    return result.modified_count > 0  # Return True if the update was successful, False otherwise

# Function to get all hardware set names
def getAllHwNames(client):
    # Get and return a list of all hardware set names
    collection = databaseHelpers.access_collection(client, "HardwareSets")
    return [hw['hwName'] for hw in collection.find({}, {"_id": 0, "hwName": 1})]

# Function to return hardware to a hardware set
def returnSpace(client, hwSetName, amount):
# Return a certain amount of hardware and update availability
    collection = databaseHelpers.access_collection(client, "HardwareSets")
    hardware_set = collection.find_one({"hwName": hwSetName})
    if not hardware_set:
         return {"success":False,"message":"Invalid hardware"} # Hardware set does not exist
    result = collection.update_one(
         {"hwName": hwSetName},
         {"$inc": {"availability": amount}}
    )

    if result.modified_count > 0:
        return {"success":True, "message":"Check In Complete"}  # Return True if the update was successful, False otherwise
    else:
         return {"success":False, "message":"Check in Failed "}  # Return True if the update was successful, False otherwise