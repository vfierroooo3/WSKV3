# hardware_client.py
import os
import base64
from functools import lru_cache
from urllib.parse import urlsplit

import grpc
import hardware_pb2
import hardware_pb2_grpc

HARDWARE_TIMEOUT_SECONDS = 5.0

@lru_cache(maxsize=1)
def _hardware_stub():
    url = urlsplit(os.environ["HARDWARE_API_URL"].strip())
    if url.scheme != "https" or not url.hostname:
        raise ValueError("HARDWARE_API_URL must be an HTTPS URL")

    target = f"{url.hostname}:{url.port or 443}"
    channel = grpc.secure_channel(target, grpc.ssl_channel_credentials())
    return hardware_pb2_grpc.HardwareServiceStub(channel)

def _hardware_metadata():
    username = os.environ["HARDWARE_API_USERNAME"]
    password = os.environ["HARDWARE_API_PASSWORD"]
    credentials = base64.b64encode(
        f"{username}:{password}".encode("utf-8")
    ).decode("ascii")
    return (("authorization", f"Basic {credentials}"),)

def get_hardware_checkouts_list(
    hardware_project_id: str,
    *,
    page: int = 1,
    size: int = 100,
) -> list:
    if not hardware_project_id:
        raise ValueError("hardware_project_id are required")

    request = hardware_pb2.ListCheckoutsRequest(
        project_id=hardware_project_id,
        outstanding=True,
        page=page,
        size=size,
    )
    response = _hardware_stub().ListCheckouts(
        request,
        timeout=5.0,
        metadata=_hardware_metadata(),
    )
    return list(response.items)

def get_hardware_allocations_list(
    hardware_project_id: str,
    *,
    page: int = 1,
    size: int = 100,
) -> hardware_pb2.ListAllocationsResponse:

    if not hardware_project_id:
        raise ValueError("hardware_project_id are required")

    request = hardware_pb2.ListAllocationsRequest(
        project_id=hardware_project_id,
        page=page,
        size=size,
    )

    return _hardware_stub().ListAllocations(
        request,
        timeout=HARDWARE_TIMEOUT_SECONDS,
        metadata=_hardware_metadata(),
    )

def return_checkout(
    checkout_id: str,
    quantity: int,
    expected_version: int,
    reason: str = "Returning outstanding hardware before project deletion",
    *,
    request_id: str,
):
    checkout_id = checkout_id.strip()
    reason = reason.strip()

    request = hardware_pb2.ReturnCheckoutRequest(
        checkout_id=checkout_id,
        quantity=quantity,
        expected_version=expected_version,
        reason=reason,
        request_id=request_id
    )
    return _hardware_stub().ReturnCheckout(
        request,
        timeout=5.0,
        metadata=_hardware_metadata(),
    )

def release_project_allocation(
    hardware_id: str,
    project_id: str,
    *,
    request_id: str
):
    request = hardware_pb2.AllocateHardwareRequest(
        hardware_id=hardware_id,
        project_id=project_id,
        quantity=0,
        reason="Release hardware reservation before project deletion",
        request_id=request_id
    )

    return _hardware_stub().AllocateHardware(
        request,
        timeout=5.0,
        metadata=_hardware_metadata(),
    )