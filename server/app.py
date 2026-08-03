# Import necessary libraries and modules
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import custom modules for database interactions
import usersDatabase
import projectsDatabase
import hardwareDatabase

# Initialize a new Flask web application
app = Flask(__name__)
CORS(app) # using cors is supposed to help remedy differences in port of flask and react

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    # Extract data from request
    data = request.get_json()

    # Attempt to log in the user using the usersDB module
    result = usersDatabase.login(
        data['userId'],
        data['password']
    )

    # Return a JSON response {success, message, userId on successful login}
    return jsonify(result)


# Route for joining an existing project
@app.route('/join_project', methods=['POST'])
def join_project():
    # Extract data from request
    data = request.get_json()

    # Attempt to join the project using the usersDB module
    result = usersDatabase.joinProject(
        data['userId'],
        data['projectId']
    )

    # Return a JSON response {success, message}
    return jsonify(result)

# Route for creating a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    # Extract data from request
    data = request.get_json()

    # Attempt to add the user using the usersDB module
    result = usersDatabase.addUser(
        data['userId'],
        data['password']
    )

    # Return a JSON response {success, message, insertedId}
    return jsonify(result)

# Route for getting the list of a user's projects
@app.route('/get_user_projects_list', methods=['POST'])
def get_user_projects_list():
    # Extract data from request
    data = request.get_json()
    # Fetch the user's projects using the usersDB module
    result = usersDatabase.getUserProjectsList(
        data['userId']
    )

    # Return a JSON response {success, message, projects}
    return jsonify(result)


# Route for creating a new project
@app.route('/create_project', methods=['POST'])
def create_project():
    # Extract Data from Request
    data = request.get_json()

    # Create the project document itself 
    result = projectsDatabase.createProject(
        data['projectName'],
        data['projectId'], 
        data['description']
    )

    # If creation worked, add creator to project (join project)
    if result['success']:
        result = usersDatabase.joinProject(
            data['userId'], 
            data['projectId']
        )

    # Return a JSON response: {success, message}
    return jsonify(result)

# Route for getting project information (query)
@app.route('/get_project_info', methods=['POST'])
def get_project_info():
    # Extract data from request
    data = request.get_json()

    # Fetch project information using the projectsDB module
    result = projectsDatabase.getProjectInfo(
        data['projectId']
    )

    # Return a JSON response {success, project} (whole project object)
    return jsonify(result)

# Route for getting hardware information
@app.route('/get_hw_info', methods=['GET'])
def get_hw_info():
    # Extract data from request
    # We don't need to extract any data since the function grabs everything
    # Fetch hardware set information using the hardwareDB module
    result = hardwareDatabase.getAllHardwareSets()

    # Return a JSON response
    return jsonify({"HardwareSets": result})

# Route for checking out hardware
@app.route('/check_out', methods=['POST'])
def check_out():
    # Extract data from request
    data = request.get_json()

    # Attempt to check out the hardware using the projectsDB module
    result = projectsDatabase.checkOutHW(
        data['projectId'],
        data['hwSetName'],
        data['qty']
    )

    # Return a JSON response
    return jsonify(result)

# Route for checking in hardware
@app.route('/check_in', methods=['POST'])
def check_in():
    # Extract data from request
    data = request.get_json()

    # Attempt to check in the hardware using the projectsDB module
    result = projectsDatabase.checkInHW(
        data['projectId'],
        data['hwSetName'],
        data['qty']
    )

    # Return a JSON response
    return jsonify(result)


# Not Used functions:

# Route for getting all hardware names
# @app.route('/get_all_hw_names', methods=['POST'])
# def get_all_hw_names():
#     # Fetch all hardware names using the hardwareDB module
#     result = hardwareDatabase.getAllHwNames()
#     # Return a JSON response
#     return jsonify({"hwNames": result})

# Route for creating a new hardware set
# @app.route('/create_hardware_set', methods=['POST'])
# def create_hardware_set():
#     # Extract data from request
#     data = request.get_json()
#     # Attempt to create the hardware set using the hardwareDB module
#     result = hardwareDatabase.createHardwareSet(
#         data['hwSetName'], 
#         data['initCapacity']
#     )
#     # Return a JSON response
#     return jsonify(result)

# Route for checking the inventory of projects
# @app.route('/api/inventory', methods=['GET'])
# def check_inventory():
#     # Fetch all projects from the HardwareCheckout.Projects collection
#     result = projectsDatabase.getAllProjects()
#     # Return a JSON response
#     return jsonify(result)

if __name__ == '__main__':
    app.run()

