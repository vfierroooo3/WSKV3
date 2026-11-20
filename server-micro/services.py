from uuid import uuid4
from pymongo.errors import DuplicateKeyError
from database import project_db
import hardware_client
import grpc

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
        {"_id": 0, "projectId": 1, "projectName": 1, "orgId": 1, "joined_users": 1},
    ))

def get_project(org_id: str, project_id: str) -> dict:
    project = projects_collection.find_one(
        {"projectId": project_id, "orgId": org_id},
        {"_id": 0},
    )
    if project is None:
        raise ProjectError("NOT_FOUND", "Project not found")
    return project

def delete_project(org_id: str, project_id: str, user_id: str) -> None:
    # 1. Confirm that the caller is the project creator.
    project = get_project(org_id, project_id)

    if project.get("creatorId") != user_id:
        raise ProjectError(
            "PERMISSION_DENIED",
            "Only the project creator can delete this project",
        )

    hardware_project_id = f"{org_id}:{project_id}"

    try:
        # 2. Reject deletion if any hardware is still checked out.
        checkouts = hardware_client.get_hardware_checkouts_list(
            hardware_project_id,
            page=1,
            size=1,
        )
        print(checkouts)
        if checkouts:
            raise ProjectError(
                "FAILED_PRECONDITION",
                "Return checked-out hardware before deleting this project",
            )

        # 3. Read all allocation pages before releasing reservations.
        allocations = []
        page = 1

        while True:
            response = hardware_client.get_hardware_allocations_list(
                hardware_project_id,
                page=page,
                size=100,
            )
            allocations.extend(response.items)

            if len(allocations) >= response.total:
                break

            if not response.items:
                raise ProjectError(
                    "FAILED_PRECONDITION",
                    "Hardware service returned incomplete allocations",
                )

            page += 1

        # Validate every allocation before making any changes.
        for allocation in allocations:
            if (
                allocation.project_id != hardware_project_id
                or not allocation.hardware_id
                or allocation.quantity < 0
                or allocation.out < 0
            ):
                raise ProjectError(
                    "FAILED_PRECONDITION",
                    "Hardware service returned an unexpected allocation",
                )

            if allocation.out > 0:
                raise ProjectError(
                    "FAILED_PRECONDITION",
                    "Return checked-out hardware before deleting this project",
                )

        # 4. Release each positive reservation by setting it to zero.
        hardware_ids = {
            item.hardware_id
            for item in allocations
            if item.quantity > 0
        }

        for hardware_id in sorted(hardware_ids):
            hardware_client.release_project_allocation(
                hardware_id=hardware_id,
                project_id=hardware_project_id,
                request_id=uuid4().hex,
            )

    except grpc.RpcError as exc:
        status = exc.code()
        raise ProjectError(
            status.name if status else "UNKNOWN",
            "Hardware cleanup failed. Project was kept.",
        ) from exc

    # 5. Delete only after all reservations have been released.
    result = projects_collection.delete_one({
        "orgId": org_id,
        "projectId": project_id,
        "creatorId": user_id,
    })

    if result.deleted_count == 0:
        raise ProjectError(
            "NOT_FOUND",
            "Project no longer matches the delete request",
        )