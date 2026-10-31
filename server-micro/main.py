from database import project_db
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ProjectCreate, ProjectAction, ProjectSearch
from exception_handlers import register_exception_handlers
import httpx
from hardware_client import get_hardware_name

app = FastAPI()
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # After frontend deployed URL
        # "https://your-frontend.com",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def project_info(projectId: str, orgId: str):
    project = projects_collection.find_one(
        {
            "projectId": projectId,
            "orgId": orgId
        },
        {"_id": 0}
    )
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    
    hardware_names = {}
    #TODO waiting for the hw team provide the api
    # async with httpx.AsyncClient(timeout=10.0) as client:
    #     for hardware in project.get("hardwareList", []):
    #         hardware_id = hardware["hardwareId"]
    #         if hardware_id not in hardware_names:
    #             hardware_names[hardware_id] = await get_hardware_name(
    #                 client,
    #                 hardware_id
    #             )

    #         hardware["hardwareName"] = hardware_names[hardware_id]

    return {
        "projectInfo": project
    }