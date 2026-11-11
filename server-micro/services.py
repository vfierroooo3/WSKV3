from pymongo.errors import DuplicateKeyError
from database import project_db

projects_collection = project_db["projects"]

class ProjectError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code

def ensure_indexes():
    projects_collection.create_index(
        [("projectId", 1), ("orgId", 1)],
        unique=True,
    )

def create_project(project_data: dict) -> None:
    document = {
        **project_data,
        "joined_users": [project_data["creatorId"]],
    }
    try:
        projects_collection.insert_one(document)
    except DuplicateKeyError as exc:
        raise ProjectError("ALREADY_EXISTS", "Project already exists") from exc

def join_project(org_id: str, project_id: str, user_id: str) -> None:
    result = projects_collection.update_one(
        {"projectId": project_id, "orgId": org_id},
        {"$addToSet": {"joined_users": user_id}},
    )
    if result.matched_count == 0:
        raise ProjectError("NOT_FOUND", "Project not found")
    if result.modified_count == 0:
        raise ProjectError("ALREADY_EXISTS", "User already joined this project")

def leave_project(org_id: str, project_id: str, user_id: str) -> None:
    result = projects_collection.update_one(
        {"projectId": project_id, "orgId": org_id},
        {"$pull": {"joined_users": user_id}},
    )
    if result.matched_count == 0:
        raise ProjectError("NOT_FOUND", "Project not found")
    if result.modified_count == 0:
        raise ProjectError(
            "FAILED_PRECONDITION", "User is not a member of this project"
        )

def search_projects(org_id="", project_id="", user_id="") -> list[dict]:
    filters = {}
    for field, value in (
        ("orgId", org_id),
        ("projectId", project_id),
        ("joined_users", user_id),
    ):
        if value and value.strip():
            filters[field] = value.strip()

    return list(projects_collection.find(
        filters,
        {"_id": 0, "projectId": 1, "projectName": 1, "orgId": 1},
    ))

def get_project(org_id: str, project_id: str) -> dict:
    project = projects_collection.find_one(
        {"projectId": project_id, "orgId": org_id},
        {"_id": 0},
    )
    if project is None:
        raise ProjectError("NOT_FOUND", "Project not found")
    return project