# Import necessary libraries and modules
from pymongo import MongoClient

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

# Function to query a project by its ID
def queryProject(client, projectId):

    # Query and return a project from the database
    projects = databaseHelpers.access_collection(client,"Projects")
    return projects.find_one({"projectId":projectId})

# Function to create a new project
def createProject(client, projectName, projectId, description):
    # Check if project already exists
    project =queryProject(client,projectId)
    if project:
        return {"success":False,
                'message':"ProjectId already in use"}

    # create new project
    project_doc = {
        'projectName': projectName,
            'projectId': projectId,
            'description': description,
            'hwSets': {"HW1": 0, "HW2": 0}, # change this to match our hardware names?
            'users': []
            }

    # access and add to projects
    projects = databaseHelpers.access_collection(client,"Projects")
    projects.insert_one(project_doc)
    return {"success":True,
            "message":"Project Created",
             "projectId":projectId }

# Function to add a user to a project
def addUser(client, projectId, userId):

    # Check if the project exists
    project =queryProject(client,projectId)
    if not project:
            return {"success":False,
                    'message':"Project does not exist"}

    # Prevent same user from being added twice
    if userId in project.get("users",[]):
        return ({"success":False,
                  "message":"User is already a member of the project"})
    projects = databaseHelpers.access_collection(client,"Projects")

    # append user to project
    projects.update_one(
            {"projectId": projectId},
            {"$push": {"users": userId}}
    )
    return {"success":True,
            "message":"User successfully added to project"}

# Function to update hardware usage in a project 
def updateUsage(client, projectId, hwSetName):
    # Used to add a new type of hardware set(beyond our two) to project if needed in future
    projects = databaseHelpers.access_collection(client,"Projects")
    projects.update_one(
        {"projectId":projectId},

        # adds in new hw set type to project with starting value of zero
        {"$set": {f"hwSets.{hwSetName}": 0}}

    )
    return {"success": True, "message": "New hardware set added to project"}
    #TO DO: Add error checks to ensure project exists, hardware set is not already in project

# Function to check out hardware for a project
def checkOutHW(client, projectId, hwSetName, qty, userId):
    # Check out hardware for the specified project and update availability
    pass
    # likely will need to call funcs from hardware to update capacity/availability

# Function to check in hardware for a project
def checkInHW(client, projectId, hwSetName, qty, userId):
    # Check in hardware for the specified project and update availability
    pass

