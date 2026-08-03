import databaseHelpers

'''
Structure of Hardware Set entry:
HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
}
'''

# Function to request space from a hardware set
def requestSpace(hwSetName, amount):
    # Request a certain amount of hardware and update availability
    collection = databaseHelpers.access_collection("HardwareSets")

    hardware_set = collection.find_one({"hwName": hwSetName})

    if not hardware_set:
        return {
            "success": False, 
            "message": "Invalid hardware"
        }
    
    if hardware_set['availability'] < amount:
        return {
            "success": False, 
            "message": "Not enough availability"
        }

    result = collection.update_one(
        {"hwName": hwSetName},
        {"$inc": {"availability": -amount}}
    )
    if result.modified_count > 0:
        return {
            "success": True, 
            "message": "Hardware successfully checked out"
        }
    else:
        return {
            "success": False, 
            "message": "Check out failed"
        }

# Function to return hardware to a hardware set
def returnSpace(hwSetName, amount):
    # Return a certain amount of hardware and update availability
    collection = databaseHelpers.access_collection("HardwareSets")

    hardware_set = collection.find_one({"hwName": hwSetName})

    if not hardware_set:
        return {
            "success": False, 
            "message": "Invalid hardware"
        } 

    result = collection.update_one(
        {"hwName": hwSetName},
        {"$inc": {"availability": amount}}
    )

    if result.modified_count > 0:
        return {
            "success": True, 
            "message": "Check In Complete"
        }
    else:
        return {
            "success": False, 
            "message": "Check In Failed"
        }

#Function for getting hardware information
def getAllHardwareSets():
    # Get and return full details for all hardware sets
    collection = databaseHelpers.access_collection("HardwareSets")
    return list(collection.find({}, {"_id": 0}))

# Function to create a new hardware set
def createHardwareSet(hwSetName, initCapacity):
    # Create a new hardware set in the database
    collection = databaseHelpers.access_collection("HardwareSets")

    # Check if hardware set already exists
    existing = collection.find_one({"hwName": hwSetName})
    if existing:
        return {"success": False, "message": "Hardware set already exists"}

    hardwareSet = {
        "hwName": hwSetName,
        "capacity": initCapacity,
        "availability": initCapacity
    }

# Not Used functions:

#     result = collection.insert_one(hardwareSet)
#     return {
#         "success": True, 
#         "message": "Hardware set created", 
#         "insertedId": str(result.inserted_id)
#     }

# Function to update the availability of a hardware set
# def updateAvailability(hwSetName, newAvailability):
#     # Update the availability of an existing hardware set
#     collection = databaseHelpers.access_collection("HardwareSets")

#     result = collection.update_one(
#         {"hwName": hwSetName},
#         {"$set": {"availability": newAvailability}}
#     )

#     if result.modified_count > 0:
#         return {
#             "success": True, 
#             "message": "Availability updated"
#         }
#     else:
#         return {
#             "success": False, 
#             "message": "Update failed"
#         }
    
# Function to get all hardware set names
# def getAllHwNames():
#     # Get and return a list of all hardware set names
#     collection = databaseHelpers.access_collection("HardwareSets")

#     return [hw['hwName'] for hw in collection.find({}, {"_id": 0, "hwName": 1})]

# Function to query a hardware set by its name
# def queryHardwareSet(hwSetName):
#     # Query and return a hardware set from the database
#     collection = databaseHelpers.access_collection("HardwareSets")

#     return collection.find_one({"hwName": hwSetName})