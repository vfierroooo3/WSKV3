"""gRPC server for the Projects microservice (contract: protos/projects.proto).

Runs next to the REST API (main.py) from the same image and calls the same
logic, so REST /docs and gRPC always agree. Other services (like the frontend
team's BFF) call this one; REST stays for /docs and manual testing.

Run locally (from server-micro/):
    python generate_protos.py
    python grpc_server.py            # listens on 0.0.0.0:50051 (GRPC_PORT)

Try it (reflection is on, so no .proto needed):
    grpcurl -plaintext localhost:50051 list
    grpcurl -plaintext -d '{"category": "Microcomputers, Handheld, Laptop, and Notebook"}' \
        localhost:50051 projects.v1.ProjectsService/GetUnitPrice

Adding an RPC: write a method on ProjectsService with the same name as in the
.proto, call the shared function, and raise errors with abort(). RPCs that
aren't written yet answer UNIMPLEMENTED automatically.
"""
import logging
import os
from concurrent import futures
from pathlib import Path

import grpc
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure, PyMongoError
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from grpc_reflection.v1alpha import reflection

import projects_pb2
import projects_pb2_grpc
import services
from notifications import notify
from unit_price import NOT_AVAILABLE, austin_unit_price

# Same .env as the REST app (AZURE_SQL_*, MONGODB_URI) for local runs; Azure
# passes these as app settings instead.
load_dotenv(Path(__file__).with_name(".env"))

log = logging.getLogger("grpc_server")

SERVICE_NAME = projects_pb2.DESCRIPTOR.services_by_name["ProjectsService"].full_name
PORT = int(os.environ.get("GRPC_PORT", "50051"))
MAX_WORKERS = int(os.environ.get("GRPC_MAX_WORKERS", "10"))

# Novu calls run here so a slow notification never delays the RPC response
# (same idea as the REST app's BackgroundTasks).
notification_pool = futures.ThreadPoolExecutor(max_workers=4)


class RpcError(Exception):
    """Raise from an RPC to return a specific gRPC status code and message."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


def invalid_argument(message):
    return RpcError(grpc.StatusCode.INVALID_ARGUMENT, message)


def not_found(message):
    return RpcError(grpc.StatusCode.NOT_FOUND, message)


def already_exists(message):
    return RpcError(grpc.StatusCode.ALREADY_EXISTS, message)


def failed_precondition(message):
    return RpcError(grpc.StatusCode.FAILED_PRECONDITION, message)


def unavailable(message):
    return RpcError(grpc.StatusCode.UNAVAILABLE, message)


def handle_errors(rpc):
    """Turn RpcError into its status code and anything unexpected into INTERNAL,
    so every RPC follows the error table in the .proto."""
    def wrapper(self, request, context):
        try:
            return rpc(self, request, context)
        except RpcError as err:
            context.abort(err.code, err.message)
        except Exception:
            if context.code() not in (None, grpc.StatusCode.OK):
                raise  # the RPC already called context.abort() itself
            log.exception("%s failed", rpc.__name__)
            context.abort(grpc.StatusCode.INTERNAL, "unexpected server error")
    wrapper.__name__ = rpc.__name__
    return wrapper


def call_service(operation, *args):
    """Run a services.py function and map its errors to gRPC status codes.
    services.ProjectError carries the status code name (e.g. "NOT_FOUND")."""
    try:
        return operation(*args)
    except services.ProjectError as err:
        raise RpcError(grpc.StatusCode[err.code], str(err))
    except ConnectionFailure:  # includes AutoReconnect and server selection timeouts
        log.exception("MongoDB unreachable in %s", operation.__name__)
        raise unavailable("project database is unavailable right now")
    except PyMongoError:
        log.exception("MongoDB error in %s", operation.__name__)
        raise RpcError(grpc.StatusCode.INTERNAL, "project database operation failed")


def require(value, field):
    """Return value stripped, or raise INVALID_ARGUMENT if it's blank."""
    value = value.strip()
    if not value:
        raise invalid_argument(f"{field} is required")
    return value


def notify_creator(workflow_id, org_id, project_id, user_id):
    """Tell the project's creator someone joined or left (never raises)."""
    try:
        project = services.get_project(org_id, project_id)
    except Exception:
        log.exception("Could not look up %s/%s for notification", org_id, project_id)
        return
    creator_id = project.get("creatorId")
    if not creator_id or creator_id == user_id:
        return
    notification_pool.submit(notify, workflow_id, [creator_id], {
        "orgId": org_id,
        "projectId": project_id,
        "projectName": project.get("projectName", ""),
        "userId": user_id,
    })


def unit_price_source(result):
    """REST returns stats or "not available"; gRPC returns available + stats."""
    if result == NOT_AVAILABLE or not isinstance(result, dict):
        return projects_pb2.SourceUnitPrice(available=False)
    return projects_pb2.SourceUnitPrice(
        available=True,
        stats=projects_pb2.PriceStats(
            median=result["median"],
            low=result["low"],
            high=result["high"],
            purchases=result["purchases"],
        ),
    )


class ProjectsService(projects_pb2_grpc.ProjectsServiceServicer):

    # ------------------------------------------------ projects (MongoDB Atlas)

    @handle_errors
    def CreateProject(self, request, context):
        project = {
            "orgId": require(request.org_id, "org_id"),
            "projectId": require(request.project_id, "project_id"),
            "projectName": require(request.project_name, "project_name"),
            "projectDesc": require(request.project_desc, "project_desc"),
            "creatorId": require(request.creator_id, "creator_id"),
            "budget": request.budget,
            "hardwareList": [],
        }
        if request.budget < 0:
            raise invalid_argument("budget must be >= 0")
        for item in request.hardware_list:
            if not item.hardware_id.strip() or item.allocation <= 0:
                raise invalid_argument(
                    "each hardware item needs a hardware_id and allocation > 0")
            project["hardwareList"].append(
                {"hardwareId": item.hardware_id.strip(), "allocation": item.allocation})
        call_service(services.create_project, project)
        return projects_pb2.CreateProjectResponse()

    @handle_errors
    def JoinProject(self, request, context):
        return self._update_membership(request, services.join_project, "member-joined")

    @handle_errors
    def LeaveProject(self, request, context):
        return self._update_membership(request, services.leave_project, "member-left")

    def _update_membership(self, request, operation, workflow_id):
        org_id = require(request.org_id, "org_id")
        project_id = require(request.project_id, "project_id")
        user_id = require(request.user_id, "user_id")
        call_service(operation, org_id, project_id, user_id)
        notify_creator(workflow_id, org_id, project_id, user_id)
        return projects_pb2.MembershipResponse()

    @handle_errors
    def SearchProjects(self, request, context):
        projects = call_service(
            services.search_projects, request.org_id, request.project_id, request.user_id)
        return projects_pb2.SearchProjectsResponse(project_list=[
            projects_pb2.ProjectSummary(
                project_id=p.get("projectId", ""),
                project_name=p.get("projectName", ""),
                org_id=p.get("orgId", ""),
                joined_users=p.get("joined_users", []),
            )
            for p in projects
        ])

    @handle_errors
    def GetProject(self, request, context):
        project = call_service(
            services.get_project,
            require(request.org_id, "org_id"),
            require(request.project_id, "project_id"),
        )
        return projects_pb2.GetProjectResponse(project_info=projects_pb2.Project(
            org_id=project.get("orgId", ""),
            project_id=project.get("projectId", ""),
            project_name=project.get("projectName", ""),
            project_desc=project.get("projectDesc", ""),
            creator_id=project.get("creatorId", ""),
            budget=project.get("budget", 0),
            hardware_list=[
                projects_pb2.HardwareItem(
                    hardware_id=item.get("hardwareId", ""),
                    allocation=item.get("allocation", 0),
                )
                for item in project.get("hardwareList", [])
            ],
            joined_users=project.get("joined_users", []),
        ))

    # ------------------------------------------------ price context

    @handle_errors
    def GetUnitPrice(self, request, context):
        category = request.category.strip()
        if not category:
            raise invalid_argument("category is required")
        try:
            austin = austin_unit_price(category)
        except Exception:
            log.exception("Azure SQL query failed for GetUnitPrice")
            raise unavailable("price data is unavailable right now")
        return projects_pb2.GetUnitPriceResponse(
            category=category,
            austin=unit_price_source(austin),
            dallas=projects_pb2.SourceUnitPrice(available=False),
            texas=projects_pb2.SourceUnitPrice(available=False),
        )
    
    @handle_errors
    def GetBudgetContext(self, request, context):
        if not request.items:
            raise invalid_argument("items list cannot be empty")

        item_results = []
        total_low = 0.0
        total_typical = 0.0
        total_high = 0.0
        has_valid_estimates = False
        unpriced_items_count = 0

        for item in request.items:
            if item.quantity <= 0:
                raise invalid_argument("quantity must be > 0")

            desc = item.description.strip()
            # Placeholder matcher logic from the REST app
            matched_category, confidence = (desc, 1.0) if desc else (None, 0.0)

            item_kwargs = {
                "description": desc,
                "quantity": item.quantity,
                "priced": False,
                "confidence": 0.0
            }

            if matched_category:
                try:
                    price_data = austin_unit_price(matched_category)
                except Exception:
                    log.exception("Azure SQL query failed for GetBudgetContext")
                    raise unavailable("price data is unavailable right now")

                if isinstance(price_data, dict):
                    e_low = round(price_data["low"] * item.quantity, 2)
                    e_typ = round(price_data["median"] * item.quantity, 2)
                    e_high = round(price_data["high"] * item.quantity, 2)

                    item_kwargs.update({
                        "priced": True,
                        "matched_category": matched_category,
                        "confidence": confidence,
                        "unit_price": projects_pb2.PriceStats(
                            median=price_data["median"],
                            low=price_data["low"],
                            high=price_data["high"],
                            purchases=price_data["purchases"],
                        ),
                        "estimated_cost": projects_pb2.CostRange(
                            low=e_low,
                            typical=e_typ,
                            high=e_high
                        )
                    })

                    total_low += e_low
                    total_typical += e_typ
                    total_high += e_high
                    has_valid_estimates = True
                else:
                    unpriced_items_count += 1
            else:
                unpriced_items_count += 1

            item_results.append(projects_pb2.ItemEstimate(**item_kwargs))

        response = projects_pb2.GetBudgetContextResponse(
            org_id=request.org_id,
            budget=request.budget,
            items=item_results,
            unpriced_items=unpriced_items_count
        )

        if has_valid_estimates:
            response.total_estimate.CopyFrom(projects_pb2.CostRange(
                low=round(total_low, 2),
                typical=round(total_typical, 2),
                high=round(total_high, 2)
            ))

        if unpriced_items_count == 0:
            response.within_budget = (total_typical <= request.budget)

        return response

    # Still to add (they return UNIMPLEMENTED until then):
    #   Valentina: GetDepartmentSpend


def build_server(port=PORT):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    projects_pb2_grpc.add_ProjectsServiceServicer_to_server(ProjectsService(), server)

    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    for name in ("", SERVICE_NAME):
        health_servicer.set(name, health_pb2.HealthCheckResponse.SERVING)

    reflection.enable_server_reflection(
        (SERVICE_NAME, health_pb2.DESCRIPTOR.services_by_name["Health"].full_name,
         reflection.SERVICE_NAME),
        server,
    )
    bound_port = server.add_insecure_port(f"0.0.0.0:{port}")
    return server, bound_port


def serve():
    logging.basicConfig(level=logging.INFO)
    try:
        services.ensure_indexes()
    except PyMongoError:
        log.exception("Could not create MongoDB indexes; continuing")
    server, port = build_server()
    server.start()
    log.info("gRPC server listening on port %s", port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
