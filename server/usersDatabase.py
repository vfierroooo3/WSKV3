# Import necessary libraries and modules
from pymongo import MongoClient

import projectsDatabase
import databaseHelpers

'''
Structure of User entry:
User = {
    'userId': userId,
    'password': password,
    'projects': [project1_ID, project2_ID, ...]
}
'''

# Function to add a new user
def addUser(client, userId, password):

    # Does a user with this userId already exist?
    existing_user = __queryUser(client, userId)
    if existing_user:
        return {'success': False, 'message': 'UserId already taken'}

    # Add a new user to the database (add a new user document)
    user_doc ={
            'userId': userId,
            'password':password,
            'projects': []
            }

    # Insert new user 
    users = databaseHelpers.access_collection(client, "Users")
    users.insert_one(user_doc)

    return {'success':True, 'message': 'User created','insertedId': userId}

# Helper function to query a user by userId
def __queryUser(client, userId):
    # Query and return a user from the database

    # Access database and users collection
    users = databaseHelpers.access_collection(client,"Users")

    # find a user
    return users.find_one({"userId":userId})

    

# Function to log in a user
def login(client, userId, password):
    # Authenticate a user and return login status

    # Check that a user exists
    existing_user = __queryUser(client,userId)
    if not existing_user:
        return {'success': False, 'message': 'Invalid UserId or Password'}

    # Check that the password matches
    if existing_user['password'] == password:
        return {'success':True,'message':'Login successful'}
    else:
        return {'success': False, 'message': 'Invalid UserId or Password'}

# Function to add a project to a user
def joinProject(client, userId, projectId):
    # Add a user to a project by first adding the project information to the user document
    # Then add the user to the project's document by calling it from the module

    # Check if the project exists
    project =projectsDatabase.queryProject(client,projectId)
    if not project:
            return {"success":False,
                    'message':"Project does not exist"}

    # Check if the user exists
    user = __queryUser(client,userId)
    if not user:
        return {"success":False,
                "message":"User does not exist"}

    # Prevent the same project from being added twice to the user
    if projectId in user.get("projects",[]):
        return ({"success":False,
                  "message":"User is already a member of the project"})
    
    users = databaseHelpers.access_collection(client,"Users")

    # Append project to user
    users.update_one(
            {"userId": userId},
            {"$push": {"projects": projectId}}
    )

    # Call the project function to add this user to that project's information
    projectsDatabase.addUser(client, projectId, userId)


    return {"success":True,
                "message":"User successfully added to project"}



# Function to get the list of projects for a user
def getUserProjectsList(client, userId):
    # Get and return the list of projects a user is part of
    user = __queryUser(client,userId)

    # Check if user exists
    if not user:
        return {"success":False, 
                "message":'User does not exist'}

    # Access and return user's projects
    return {"success":True,
            "projects":user.get("projects",[])}

