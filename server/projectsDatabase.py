import hardwareDatabase
import databaseHelpers

'''
Structure of Project entry:
Project = {
    'projectName': projectName,
    'projectId': projectId,
    'description': description,
    'hwSets': {HW1: 0, HW2: 10, ...},
    'users': [user1, user2, ...]
}
'''

# Function to query a project by its ID (helper function)
def queryProject(projectId):
    # Query and return a project from the database
    projects = databaseHelpers.access_collection("Projects")
    
    return projects.find_one({"projectId": projectId}, {"_id": 0})

# Function for the /get_project_info route specifically (because need success messages for api)
def getProjectInfo(projectId):
    projectInfo = queryProject(projectId)
    if not projectInfo:
        return {
            "success": False, 
            "message": "Project not found"
        }
    return {
        "success": True, 
        "project": projectInfo
    }

# Function to create a new project
def createProject(projectName, projectId, description):
    # Check if project already exists
    project = queryProject(projectId)
    if project:
        return {
            "success": False,
            "message": "ProjectId already in use"
        }

    # create new project
    project_doc = {
        'projectName': projectName,
        'projectId': projectId,
        'description': description,
        'hwSets': {
            "Jet": 0,
            "Helicopter": 0
        },
        'users': []
    }

    # access and add to projects
    projects = databaseHelpers.access_collection("Projects")
    projects.insert_one(project_doc)
    return {
        "success": True,
        "message": "Project Created"
    }

# Function to add a user to a project
def addUser(projectId, userId):
    # Check if the project exists
    project = queryProject(projectId)
    if not project:
        return {
            "success": False,
            "message": "Project does not exist"
        }

    # Prevent same user from being added twice
    if userId in project.get("users", []):
        return {
            "success": False,
            "message": "User is already a member of the project"
        }

    projects = databaseHelpers.access_collection("Projects")
    # append user to project
    projects.update_one(
        {"projectId": projectId},
        {"$push": {"users": userId}}
    )
    return {
        "success": True,
        "message": "User successfully added to project"
    }


# Function to check out hardware for a project
def checkOutHW(projectId, hwSetName, qty):
    # Check out hardware for the specified project and update availability
    if qty <= 0:
        return {
            "success": False, 
            "message": "Quantity must be positive"
        }

    # Check that project exists and hardware is associated with it
    project = queryProject(projectId)

    if not project:
        return {
            "success": False, 
            "message": "Invalid ProjectId"
        }

    if hwSetName not in project['hwSets']:
        return {
            "success": False, 
            "message": "Hardware not associated with project"
        }

    # Call hardware db to request space and update on hardware side
    # this checks that hardware exists and that there is enough available
    result = hardwareDatabase.requestSpace(hwSetName, qty)

    # if hardware call unsuccessful, return false + its error
    if not result['success']:
        return result

    # Update project info
    projects = databaseHelpers.access_collection("Projects")

    projects.update_one(
        {"projectId": projectId},
        {"$inc": {f"hwSets.{hwSetName}": qty}}
    )

    return {
        "success": True, 
        "message": "Hardware successfully checked out"
    }

# Function to check in hardware for a project
def checkInHW(projectId, hwSetName, qty):
    # Check in hardware for the specified project and update availability

    # Ensure positive quantity
    if qty <= 0:
        return {
            "success": False, 
            "message": "Quantity must be positive"
        }

    # Check that project exists and that the hardware set is associated with it
    project = queryProject(projectId)

    if not project:
        return {
            "success": False, 
            "message": "Invalid ProjectId"
        }

    if hwSetName not in project['hwSets']:
        return {
            "success": False, 
            "message": "Hardware not checked out"
        }

    # Make sure they are not trying to check in more than they have checked out
    if qty > project['hwSets'][hwSetName]:
        return {
            "success": False, 
            "message": "Cannot return more than checked out"
        }

    # Call hardware db to return items and update on hardware side
    result = hardwareDatabase.returnSpace(hwSetName, qty)

    if not result["success"]:
        return result

    # Update quantity in project
    projects = databaseHelpers.access_collection("Projects")

    projects.update_one(
        {"projectId": projectId},
        {"$inc": {f"hwSets.{hwSetName}": -qty}}
    )

    return {"success": True, "message": "Hardware successfully checked in"}

# Not Used functions:

# Function to update hardware usage in a project
# def updateUsage(projectId, hwSetName):
#     # Used to add a new type of hardware set (beyond our two) to project if needed in future

#     # Check that project exists
#     project = queryProject(projectId)
#     if not project:
#         return {
#             "success": False, 
#             "message": "Invalid ProjectId"
#         }

#     # Check that hardware is not already associated with it
#     if hwSetName in project.get("hwSets", {}):
#         return {
#             "success": False, 
#             "message": "Hardware already associated with project"
#         }

#     projects = databaseHelpers.access_collection("Projects")
#     projects.update_one(
#         {"projectId": projectId},
#         {"$set": {f"hwSets.{hwSetName}": 0}}
#     )
#     return {
#         "success": True,
#         "message": "New hardware set added to project"
#     }
#     # TODO: Add error checks to ensure project exists, hardware set is not already in project

# def getAllProjects():
#     # Get and return a list of all projects
#     collection = databaseHelpers.access_collection("Projects")
#     return list(collection.find({}, {"_id": 0}))