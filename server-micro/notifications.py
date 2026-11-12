"""Send notifications through Novu (our external notification service).

notify() triggers a Novu workflow (e.g. "member-joined") for one or more
subscribers. It never raises: a failed notification is logged and skipped, so
it can't break the request that caused it. Call it as a FastAPI BackgroundTask.

Settings (from .env locally, Azure secrets when deployed):
  NOVU_SECRET_KEY  required; Novu secret key (Dashboard -> API Keys)
  NOVU_API_URL     optional; defaults to https://api.novu.co
                   (EU region accounts use https://eu.api.novu.co)
"""
import logging
import os

import httpx

log = logging.getLogger(__name__)

NOVU_TIMEOUT_SECONDS = 5.0
DEFAULT_NOVU_API_URL = "https://api.novu.co"


def notify(workflow_id, subscriber_ids, payload=None):
    """Trigger a Novu workflow for each subscriber. Returns True if Novu accepted it."""
    try:
        if isinstance(subscriber_ids, str):
            subscriber_ids = [subscriber_ids]
        recipients = [{"subscriberId": str(s)} for s in subscriber_ids or [] if s]
        if not recipients:
            log.warning("notify(%s) skipped: no subscribers", workflow_id)
            return False

        secret_key = os.environ.get("NOVU_SECRET_KEY")
        if not secret_key:
            log.warning("notify(%s) skipped: NOVU_SECRET_KEY is not set", workflow_id)
            return False

        base_url = os.environ.get("NOVU_API_URL", DEFAULT_NOVU_API_URL).rstrip("/")
        response = httpx.post(
            f"{base_url}/v1/events/trigger",
            headers={"Authorization": f"ApiKey {secret_key}"},
            json={"name": workflow_id, "to": recipients, "payload": payload or {}},
            timeout=NOVU_TIMEOUT_SECONDS,
        )
        if response.status_code >= 400:
            log.error(
                "notify(%s) failed: Novu returned %s: %s",
                workflow_id, response.status_code, response.text[:300],
            )
            return False
        return True
    except Exception:
        # Never let a notification problem reach the caller.
        log.exception("notify(%s) failed", workflow_id)
        return False
