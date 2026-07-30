# Import necessary libraries and modules
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

# Import custom modules for database interactions
import usersDatabase
import projectsDatabase
import hardwareDatabase

# Define the MongoDB connection string
MONGODB_SERVER = "mongodb+srv://katierafdahl_db_user:45sfmVPrbATWYm3t@wskv3.zcpyq8u.mongodb.net/?appName=WSKV3"

# Initialize a new Flask web application
app = Flask(__name__)
CORS(app) # using cors is supposed to help remedy differences in port of flask and react

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    # Extract data from request
    data = request.get_json()
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    # Attempt to log in the user using the usersDB module
    result = usersDatabase.login(client,data['userId'],data['password'])
    # Close the MongoDB connection
    client.close()

    # Return a JSON response {success, message, userId on successful login}
    return jsonify(result)


# Route for joining an existing project
@app.route('/join_project', methods=['POST'])
def join_project():
    # Extract data from request
    data = request.get_json()
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    # Attempt to join the project using the usersDB module
    result = usersDatabase.joinProject(client,data['userId'],data['projectId'])
    # Close the MongoDB connection
    client.close()

    # Return a JSON response {success, message,userId, projectId}
    return jsonify(result)

# Route for creating a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    # Extract data from request
    data = request.get_json()
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    # Attempt to add the user using the usersDB module
    result = usersDatabase.addUser(client,data['userId'],data['password'])
    # Close the MongoDB connection
    client.close()

    # Return a JSON response {success, message, insertedId}
    return jsonify(result)

# Route for getting the list of a user's projects
@app.route('/get_user_projects_list', methods=['POST'])
def get_user_projects_list():
    # Extract data from request
    data = request.get_json()
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    # Fetch the user's projects using the usersDB module
    result = usersDatabase.getUserProjectsList(client,data['userId'])
    # Close the MongoDB connection
    client.close()

    # Return a JSON response {success, message, projects}
    return jsonify(result)


# Route for creating a new project
@app.route('/create_project', methods=['POST'])
def create_project():
    # Extract Data from Request
    data = request.get_json()
    # Connect to database
    client = MongoClient(MONGODB_SERVER)

    # Create the project document itself 
    result = projectsDatabase.createProject(
            client, data['projectName'],
            data['projectId'], data['description']
    )

    # If creation worked, add creator to project (join project)
    if result['success']:
        result = usersDatabase.joinProject(
            client, data['userId'], data['projectId']
        )
    # Close the MongoDB connection
    client.close()

    # Return a JSON response: {success, message, userId, projectId}
    return jsonify(result)

# Route for getting project information (query)
@app.route('/get_project_info', methods=['POST'])
def get_project_info():
    # Extract data from request
    data = request.get_json()
    # Connect to MongoDB
    client = MongoClient(MONGODB_SERVER)
    # Fetch project information using the projectsDB module
    result = projectsDatabase.queryProject(client,data['projectId'])
    # Close the MongoDB connection
    client.close()

    # Return a JSON response {project object}
        # (object should include projectName, projectId,description, hwSets,users)
    return jsonify(result)

# Route for getting all hardware names
@app.route('/get_all_hw_names', methods=['POST'])
def get_all_hw_names():
    # Connect to MongoDB

    # Fetch all hardware names using the hardwareDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for getting hardware information
@app.route('/get_hw_info', methods=['POST'])
def get_hw_info():
    # Extract data from request

    # Connect to MongoDB

    # Fetch hardware set information using the hardwareDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for checking out hardware
@app.route('/check_out', methods=['POST'])
def check_out():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to check out the hardware using the projectsDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for checking in hardware
@app.route('/check_in', methods=['POST'])
def check_in():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to check in the hardware using the projectsDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for creating a new hardware set
@app.route('/create_hardware_set', methods=['POST'])
def create_hardware_set():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to create the hardware set using the hardwareDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for checking the inventory of projects
@app.route('/api/inventory', methods=['GET'])
def check_inventory():
    # Connect to MongoDB

    # Fetch all projects from the HardwareCheckout.Projects collection

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Main entry point for the application
if __name__ == '__main__':
    app.run()

