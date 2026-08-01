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

    # Check if hardware set already exists
    existing = collection.find_one({"hwName": hwSetName})
    if existing:
        return {"success": False, "message": "Hardware set already exists"}

    hardwareSet = {
        "hwName": hwSetName,
        "capacity": initCapacity,
        "availability": initCapacity
    }

    result = collection.insert_one(hardwareSet)
    return {"success": True, "message": "Hardware set created", "insertedId": str(result.inserted_id)}

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
    if result.modified_count > 0:
        return {"success": True, "message": "Availability updated"}
    else:
        return {"success": False, "message": "Update failed"}

# Function to request space from a hardware set
def requestSpace(client, hwSetName, amount):
    # Request a certain amount of hardware and update availability
    collection = databaseHelpers.access_collection(client, "HardwareSets")
    hardware_set = collection.find_one({"hwName": hwSetName})
    if not hardware_set:
        return {"success": False, "message": "Invalid hardware"}
    if hardware_set['availability'] < amount:
        return {"success": False, "message": "Not enough availability"}

    result = collection.update_one(
        {"hwName": hwSetName},
        {"$inc": {"availability": -amount}}
    )
    if result.modified_count > 0:
        return {"success": True, "message": "Hardware successfully checked out"}
    else:
        return {"success": False, "message": "Check out failed"}

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
        return {"success": False, "message": "Invalid hardware"}  # Hardware set does not exist

    result = collection.update_one(
        {"hwName": hwSetName},
        {"$inc": {"availability": amount}}
    )

    if result.modified_count > 0:
        return {"success": True, "message": "Check In Complete"}
    else:
        return {"success": False, "message": "Check In Failed"}

#Function for getting hardware information
def getAllHardwareSets(client):
    # Get and return full details for all hardware sets
    collection = databaseHelpers.access_collection(client, "HardwareSets")
    return list(collection.find({}, {"_id": 0}))

