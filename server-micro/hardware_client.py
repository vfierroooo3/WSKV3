import os
import httpx
from fastapi import HTTPException


async def get_hardware_name(
    client: httpx.AsyncClient,
    hardware_id: str
) -> str:
    base_url = os.environ["HARDWARE_API_URL"].rstrip("/")

    try:
        response = await client.get(
            f"{base_url}/hardware/{hardware_id}"
        )
        response.raise_for_status()

        name = response.json()["hardwareName"]

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid hardwareName")

        return name

    except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve hardware name"
        ) from exc