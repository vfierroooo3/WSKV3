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
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from grpc_reflection.v1alpha import reflection

import projects_pb2
import projects_pb2_grpc
from unit_price import NOT_AVAILABLE, austin_unit_price

# Same .env as the REST app (AZURE_SQL_*, MONGODB_URI) for local runs; Azure
# passes these as app settings instead.
load_dotenv(Path(__file__).with_name(".env"))

log = logging.getLogger("grpc_server")

SERVICE_NAME = projects_pb2.DESCRIPTOR.services_by_name["ProjectsService"].full_name
PORT = int(os.environ.get("GRPC_PORT", "50051"))
MAX_WORKERS = int(os.environ.get("GRPC_MAX_WORKERS", "10"))


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

    # Still to add (they return UNIMPLEMENTED until then):
    #   Wei:       CreateProject, JoinProject, LeaveProject
    #   Ranya:     SearchProjects, GetProject, GetBudgetContext
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
    server, port = build_server()
    server.start()
    log.info("gRPC server listening on port %s", port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
