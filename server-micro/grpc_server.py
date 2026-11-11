# grpc_server.py
import logging
from notifications import notify
from concurrent.futures import ThreadPoolExecutor

import grpc
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from grpc_reflection.v1alpha import reflection
from pymongo.errors import AutoReconnect, ConnectionFailure, PyMongoError

import projects_pb2 as pb
import projects_pb2_grpc as rpc
import services

from database import project_db
projects_collection = project_db["projects"]

def call_service(context, operation, *args):
    try:
        return operation(*args)
    except services.ProjectError as exc:
        context.abort(grpc.StatusCode[exc.code], str(exc))
    except (AutoReconnect, ConnectionFailure):
        context.abort(grpc.StatusCode.UNAVAILABLE, "Project database unavailable")
    except PyMongoError:
        logging.exception("Project database operation failed")
        context.abort(grpc.StatusCode.INTERNAL, "Project database operation failed")


def require_project_key(request, context):
    if not request.org_id.strip():
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, "org_id is required")
    if not request.project_id.strip():
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, "project_id is required")


class ProjectsServicer(rpc.ProjectsServiceServicer):
    def __init__(self, notification_pool):
        self.notification_pool = notification_pool

    def CreateProject(self, request, context):
        require_project_key(request, context)

        if not request.project_desc.strip():
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "project_desc is required")
        if request.budget <= 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "budget is required and must be > 0"
            )

        if not request.hardware_list:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "hardware must contain at least one item",
            )

        hardware_list = []
        for item in request.hardware_list:
            if not item.hardware_id.strip() or item.allocation < 0:
                context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT,
                    "Each hardware item requires hardware_id and allocation >= 0",
                )
            hardware_list.append({
                "hardwareId": item.hardware_id,
                "allocation": item.allocation,
            })

        call_service(context, services.create_project, {
            "orgId": request.org_id,
            "projectId": request.project_id,
            "projectName": request.project_name,
            "projectDesc": request.project_desc,
            "creatorId": request.creator_id,
            "budget": request.budget,
            "hardwareList": hardware_list,
        })
        return pb.CreateProjectResponse(success=True, error_message="")

    def JoinProject(self, request, context):
        return self.update_membership(
            request, context, services.join_project, "member-joined"
        )

    def LeaveProject(self, request, context):
        return self.update_membership(
            request, context, services.leave_project, "member-left"
        )

    def update_membership(self, request, context, operation, workflow_id):
        require_project_key(request, context)
        if not request.user_id.strip():
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "user_id is required")

        args = (request.org_id, request.project_id, request.user_id)
        call_service(context, operation, *args)
        try:
            project = services.get_project(request.org_id, request.project_id)
            creator_id = project.get("creatorId")

            if creator_id and creator_id != request.user_id:
                self.notification_pool.submit(
                    notify,
                    workflow_id,
                    [creator_id],
                    {
                        "orgId": request.org_id,
                        "projectId": request.project_id,
                        "projectName": project.get("projectName", ""),
                        "userId": request.user_id,
                    },
                )
        except (services.ProjectError, PyMongoError, RuntimeError):
            logging.exception(
                "Could not schedule notification for %s/%s",
                request.org_id,
                request.project_id,
            )
        return pb.MembershipResponse(success=True, error_message="")

    def SearchProjects(self, request, context):
        projects = call_service(
            context,
            services.search_projects,
            request.org_id,
            request.project_id,
            request.user_id,
        )
        return pb.SearchProjectsResponse(project_list=[
            pb.ProjectSummary(
                project_id=project["projectId"],
                project_name=project["projectName"],
                org_id=project["orgId"],
            )
            for project in projects
        ])

    def GetProject(self, request, context):
        require_project_key(request, context)
        project = call_service(
            context, services.get_project, request.org_id, request.project_id
        )
        return pb.GetProjectResponse(project_info=pb.Project(
            org_id=project["orgId"],
            project_id=project["projectId"],
            project_name=project["projectName"],
            project_desc=project["projectDesc"],
            creator_id=project["creatorId"],
            budget=project["budget"],
            hardware_list=[
                pb.HardwareItem(
                    hardware_id=item["hardwareId"],
                    allocation=item["allocation"],
                )
                for item in project.get("hardwareList", [])
            ],
            joined_users=project.get("joined_users", []),
        ))

def serve():
    services.ensure_indexes()
    with ThreadPoolExecutor(max_workers=4) as notifications:
        with ThreadPoolExecutor(max_workers=10) as workers:
            server = grpc.server(workers)
            rpc.add_ProjectsServiceServicer_to_server(
                ProjectsServicer(notifications), server
            )

            service_name = pb.DESCRIPTOR.services_by_name["ProjectsService"].full_name
            health_service = health.HealthServicer()
            health_pb2_grpc.add_HealthServicer_to_server(health_service, server)
            health_service.set("", health_pb2.HealthCheckResponse.SERVING)
            health_service.set(service_name, health_pb2.HealthCheckResponse.SERVING)

            reflection.enable_server_reflection(
                (service_name, health.SERVICE_NAME, reflection.SERVICE_NAME),
                server,
            )
            server.add_insecure_port("0.0.0.0:50051")
            server.start()
            try:
                server.wait_for_termination()
            except KeyboardInterrupt:
                server.stop(5).wait()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()