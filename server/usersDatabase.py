# Import necessary libraries and modules
from pymongo import MongoClient

import projectsDatabase

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

    # Access the database via client
    db = client.WSKV3

    # Access users collection
    users = db.Users

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
    result = users.insert_one(user_doc)

    return {'success':True, 'message': 'User created','insertedId': str(result.inserted_id)}

# Helper function to query a user by userId
def __queryUser(client, userId):
    # Query and return a user from the database

    # Access database and users collection
    db = client.WSKV3
    users = db.Users

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

# Function to add a user to a project
def joinProject(client, userId, projectId):
    # Add a user to a specified project
    pass

# Function to get the list of projects for a user
def getUserProjectsList(client, userId):
    # Get and return the list of projects a user is part of
    pass

