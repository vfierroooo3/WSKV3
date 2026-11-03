"""POST /get_department_spend — how much a department typically spends in a year on a kind of item.

Uses the totals in the Dallas and Texas data (Austin's purchase orders have no
department column, so Austin always comes back as "not available").

Each source labels items its own way, so the request takes a keyword
(like "computer") and matches it against each source's own description columns.
The response lists the labels that matched, so callers can see what was counted.
"""
import logging
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from azure_sql import get_connection
from unit_price import MIN_PURCHASES, NOT_AVAILABLE, _percentile

router = APIRouter()
log = logging.getLogger(__name__)

MIN_KEYWORD_LENGTH = 3
MAX_MATCHED_LABELS = 5

# One row per department per fiscal year: that department's total spend on matching items.
DALLAS_SQL = """
    SELECT department, fy, SUM(chksubtot) AS spend
    FROM dbo.vw_dallas
    WHERE (UPPER(commoditydscr) LIKE ? ESCAPE '\\'
        OR UPPER(object)        LIKE ? ESCAPE '\\'
        OR UPPER(objectgroup)   LIKE ? ESCAPE '\\')
      AND chksubtot > 0
      AND department IS NOT NULL
      AND fy IS NOT NULL
    GROUP BY department, fy
"""
DALLAS_LABELS_SQL = f"""
    SELECT TOP {MAX_MATCHED_LABELS} commoditydscr, COUNT(*) AS n
    FROM dbo.vw_dallas
    WHERE (UPPER(commoditydscr) LIKE ? ESCAPE '\\'
        OR UPPER(object)        LIKE ? ESCAPE '\\'
        OR UPPER(objectgroup)   LIKE ? ESCAPE '\\')
      AND chksubtot > 0
    GROUP BY commoditydscr
    ORDER BY n DESC
"""

# Texas: "department" is the customer agency; the year comes from the billing month.
TEXAS_SQL = """
    SELECT customer, YEAR(start_time) AS yr, SUM(total_charges) AS spend
    FROM dbo.vw_texas
    WHERE (UPPER(resource_unit_group) LIKE ? ESCAPE '\\'
        OR UPPER(resource_unit)       LIKE ? ESCAPE '\\'
        OR UPPER(business_line)       LIKE ? ESCAPE '\\')
      AND total_charges > 0
      AND customer IS NOT NULL
      AND start_time IS NOT NULL
    GROUP BY customer, YEAR(start_time)
"""
TEXAS_LABELS_SQL = f"""
    SELECT TOP {MAX_MATCHED_LABELS} resource_unit_group, COUNT(*) AS n
    FROM dbo.vw_texas
    WHERE (UPPER(resource_unit_group) LIKE ? ESCAPE '\\'
        OR UPPER(resource_unit)       LIKE ? ESCAPE '\\'
        OR UPPER(business_line)       LIKE ? ESCAPE '\\')
      AND total_charges > 0
    GROUP BY resource_unit_group
    ORDER BY n DESC
"""


class DepartmentSpendRequest(BaseModel):
    keyword: Any = None

    model_config = ConfigDict(json_schema_extra={"example": {"keyword": "computer"}})


def like_pattern(keyword):
    """'%KEYWORD%' with LIKE's special characters escaped, so user text can't act as a wildcard."""
    escaped = (
        keyword.upper()
        .replace("\\", "\\\\")
        .replace("%", "\\%")
        .replace("_", "\\_")
        .replace("[", "\\[")
    )
    return f"%{escaped}%"


def summarize(rows):
    """rows = (department, year, spend). Typical yearly spend across department-years."""
    totals = sorted(float(r[2]) for r in rows if r[2] is not None and float(r[2]) > 0)
    if len(totals) < MIN_PURCHASES:
        return NOT_AVAILABLE
    return {
        "typicalYearly": round(_percentile(totals, 0.50), 2),
        "low": round(_percentile(totals, 0.25), 2),
        "high": round(_percentile(totals, 0.75), 2),
        "departments": len({r[0] for r in rows}),
        "years": sorted({int(r[1]) for r in rows}),
    }


def source_spend(cursor, spend_sql, labels_sql, pattern):
    params = (pattern, pattern, pattern)
    rows = cursor.execute(spend_sql, *params).fetchall()
    result = summarize(rows)
    if result == NOT_AVAILABLE:
        return result
    labels = cursor.execute(labels_sql, *params).fetchall()
    result["matchedLabels"] = [row[0] for row in labels if row[0]]
    return result


def department_spend(keyword):
    pattern = like_pattern(keyword)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        dallas = source_spend(cursor, DALLAS_SQL, DALLAS_LABELS_SQL, pattern)
        texas = source_spend(cursor, TEXAS_SQL, TEXAS_LABELS_SQL, pattern)
    finally:
        conn.close()
    return {"Austin": NOT_AVAILABLE, "Dallas": dallas, "Texas": texas}


@router.post("/get_department_spend")
def get_department_spend(request: DepartmentSpendRequest):
    keyword = request.keyword.strip() if isinstance(request.keyword, str) else ""
    if len(keyword) < MIN_KEYWORD_LENGTH:
        return JSONResponse(
            status_code=400,
            content={"success": False,
                     "message": f"keyword must be at least {MIN_KEYWORD_LENGTH} characters"},
        )

    try:
        spend = department_spend(keyword)
    except Exception:
        log.exception("Azure SQL query failed for /get_department_spend")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "spending data is unavailable right now"},
        )

    return {"success": True, "keyword": keyword, "departmentSpend": spend}
