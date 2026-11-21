"""When each source's data was last refreshed and verified ("data as of").

Reads dbo.etl_load_log, which the ADF pipelines write after every run
(Ranya granted the API's read-only login SELECT on it). Only SUCCESS rows
count, so after a failed refresh this still shows the last verified load,
which is exactly what the live tables are serving.

Cached for 10 minutes: the pipeline runs every 3 days, so there's no need to
query the log on every request. Never raises; returns {} if the log can't be read.
"""
import logging
import threading
import time

from azure_sql import get_connection

log = logging.getLogger(__name__)

DATA_AS_OF_SQL = """
    SELECT source_name, MAX(end_time) AS data_as_of
    FROM dbo.etl_load_log
    WHERE status = 'SUCCESS'
    GROUP BY source_name
"""
CACHE_SECONDS = 600

_lock = threading.Lock()
_cache = {"at": 0.0, "value": {}}


def _iso(value):
    return value.isoformat() if hasattr(value, "isoformat") else str(value)


def data_as_of():
    """{lowercased source_name: ISO timestamp of its last successful load}."""
    with _lock:
        if _cache["value"] and time.time() - _cache["at"] < CACHE_SECONDS:
            return _cache["value"]
    try:
        conn = get_connection()
        try:
            rows = conn.cursor().execute(DATA_AS_OF_SQL).fetchall()
        finally:
            conn.close()
        value = {str(row[0]).strip().lower(): _iso(row[1]) for row in rows if row[0] and row[1]}
    except Exception:
        log.exception("Could not read dbo.etl_load_log")
        with _lock:
            return _cache["value"]
    with _lock:
        _cache.update(at=time.time(), value=value)
    return value


def source_as_of(source):
    """Timestamp for one source (e.g. "austin"), matching names like "austin" or "pl_austin"."""
    source = source.lower()
    for name, stamp in data_as_of().items():
        if name == source or source in name:
            return stamp
    return None
