"""Look up usernames from the Users team's gRPC service (UsersService.GetUsername).

Used to fill in userName on join/leave notifications when the client didn't
send one. get_username() never raises: on any failure it returns None and the
caller falls back to the user ID.

Settings (.env locally, Azure app settings / secrets when deployed):
  USERS_API_KEY    required; the x-api-key the Users team gave us (keep it a secret)
  USERS_GRPC_ADDR  optional; defaults to the Users team's Azure container app
"""
import logging
import os
from functools import lru_cache

import grpc

import users_pb2
import users_pb2_grpc

log = logging.getLogger(__name__)

DEFAULT_USERS_GRPC_ADDR = "apad-users-grpc.bluedesert-b9b6bdd4.westus.azurecontainerapps.io:443"
SERVICE_NAME = "projects"
TIMEOUT_SECONDS = 5.0


@lru_cache(maxsize=1)
def _stub():
    addr = os.environ.get("USERS_GRPC_ADDR", DEFAULT_USERS_GRPC_ADDR)
    # TLS, same as grpc.credentials.createSsl() in Node; no https:// prefix.
    channel = grpc.secure_channel(addr, grpc.ssl_channel_credentials())
    return users_pb2_grpc.UsersServiceStub(channel)


def get_username(user_id):
    """Return the username for user_id, or None if it can't be looked up."""
    user_id = str(user_id or "").strip()
    if not user_id:
        return None
    api_key = os.environ.get("USERS_API_KEY")
    if not api_key:
        log.warning("GetUsername skipped: USERS_API_KEY is not set")
        return None
    try:
        response = _stub().GetUsername(
            users_pb2.GetUsernameRequest(user_id=user_id),
            metadata=(("x-service-name", SERVICE_NAME), ("x-api-key", api_key)),
            timeout=TIMEOUT_SECONDS,
        )
        return response.username.strip() or None
    except grpc.RpcError as e:
        code = e.code()
        if code == grpc.StatusCode.NOT_FOUND:
            log.info("GetUsername: no user %s", user_id)
        elif code == grpc.StatusCode.INVALID_ARGUMENT:
            log.info("GetUsername: user_id %r isn't numeric", user_id)
        elif code == grpc.StatusCode.UNAUTHENTICATED:
            log.error("GetUsername: Users service rejected x-service-name / x-api-key")
        else:
            log.warning("GetUsername failed for %s: %s %s", user_id, code, e.details())
        return None
    except Exception:
        log.exception("GetUsername failed for %s", user_id)
        return None


def resolve_user_name(user_name, user_id):
    """Name for notifications: the one the client sent, else the Users service's, else the ID."""
    return (user_name or "").strip() or get_username(user_id) or user_id
