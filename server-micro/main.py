from database import project_db
from pymongo.errors import PyMongoError, DuplicateKeyError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import ProjectCreate, ProjectAction, ProjectSearch

app = FastAPI()

projects_collection = project_db["projects"]
projects_collection.create_index(
    [("projectId", 1), ("orgId", 1)],
    unique=True
)

@app.post("/projects/create_project")
def create_project(project: ProjectCreate):
    project_data = project.model_dump()
    project_data["joined_users"] = [project.creatorId]

    projects_collection.insert_one(project_data)

    return {
        "success": True,
        "errorMessage": ""
    }

@app.post("/projects/join_project")
def join_project(project: ProjectAction):
    result = projects_collection.update_one(
        {
            "projectId": project.projectId,
            "orgId": project.orgId
        },
        {"$addToSet": {"joined_users": project.userId}}
    )

    check_update_result(result, "User already joined this project")

    return {
        "success": True,
        "errorMessage": ""
    }

@app.post("/projects/leave_project")
def leave_project(project: ProjectAction):
    result = projects_collection.update_one(
        {
            "projectId": project.projectId,
            "orgId": project.orgId
        },
        {"$pull": {"joined_users": project.userId}}
    )
    check_update_result(result, "User is not a member of this project")

    return {
        "success": True,
        "errorMessage": ""
    }

@app.post("/projects/search_project")
def search_projects(search: ProjectSearch):
    filters = {
        key: value.strip()
        for key, value in search.model_dump().items()
        if value is not None and value.strip() != ""
    }

    projects = list(
        projects_collection.find(
            filters,
            {
                "_id": 0,
                "projectId": 1,
                "projectName": 1,
                "orgId": 1
            }
        )
    )

    return {
        "projectList": projects
    }

def check_update_result(result, error_message):
    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=409,
            detail=error_message
        )

@app.get("/projects/{projectId}")
def project_info(projectId: str):
    project = projects_collection.find_one(
        {"projectId": projectId},
        {"_id": 0}
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return {
        "projectInfo": project
    }

def error_response(status_code, message, headers=None):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "errorMessage": message
        },
        headers=headers
    )


# HTTP Error: 404、409
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):
    return error_response(
        exc.status_code,
        str(exc.detail),
        headers=exc.headers
    )

# Input Valid Error：422
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    messages = []

    for error in exc.errors():
        field = ".".join(str(part) for part in error["loc"])
        messages.append(f"{field}: {error['msg']}")

    return error_response(
        422,
        "; ".join(messages)
    )

# Unique Key Error：409
@app.exception_handler(DuplicateKeyError)
async def duplicate_key_exception_handler(
    request: Request,
    exc: DuplicateKeyError
):
    return error_response(
        409,
        "Project already exists or another unique field conflicts"
    )

# MongoDB Error
@app.exception_handler(PyMongoError)
async def mongodb_exception_handler(
    request: Request,
    exc: PyMongoError
):
    return error_response(
        500,
        "Database operation failed"
    )