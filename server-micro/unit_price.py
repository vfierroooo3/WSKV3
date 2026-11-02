"""POST /get_unit_price — what governments typically pay per unit for a category.

Only the Austin data has quantities and unit prices, so Dallas and Texas
always come back as "not available" (see the Projects Group API Contract).
"""
import logging
import math
import os
import re
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from azure_sql import get_connection

router = APIRouter()
log = logging.getLogger(__name__)

# Typed view over stg_austin (loaded by the ADF pipeline). Override with AUSTIN_VIEW.
AUSTIN_VIEW = os.environ.get("AUSTIN_VIEW", "dbo.vw_austin")
if not re.fullmatch(r"[A-Za-z_][\w]*(\.[A-Za-z_][\w]*)?", AUSTIN_VIEW):
    raise ValueError(f"Invalid AUSTIN_VIEW: {AUSTIN_VIEW!r}")

# Category = commodity_description (e.g. "LIGHTS, EMERGENCY") or the commodity code.
# Rows with a 0 unit price / 0 quantity are price-agreement lump sums, not unit purchases.
AUSTIN_PRICES_SQL = f"""
    SELECT unit_price
    FROM {AUSTIN_VIEW}
    WHERE (UPPER(LTRIM(RTRIM(commodity_description))) = UPPER(?) OR CONVERT(varchar(50), commodity) = ?)
      AND unit_price > 0
      AND quantity > 0
"""

MIN_PURCHASES = 3
NOT_AVAILABLE = "not available"


class UnitPriceRequest(BaseModel):
    category: Any = None

    model_config = ConfigDict(json_schema_extra={"example": {"category": "Laptops"}})


def _to_price(value):
    """Turn 912, "912.00" or "$1,150.00" into a float; None if unusable."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, str):
        value = value.replace("$", "").replace(",", "").strip()
    try:
        price = float(value)
    except (TypeError, ValueError):
        return None
    # Zero-price rows exist in the Austin data (lump-sum lines); skip them.
    if not math.isfinite(price) or price <= 0:
        return None
    return price


def _percentile(sorted_values, p):
    """Linear-interpolation percentile (same method as numpy's default)."""
    k = (len(sorted_values) - 1) * p
    lower = math.floor(k)
    upper = min(lower + 1, len(sorted_values) - 1)
    return sorted_values[lower] + (sorted_values[upper] - sorted_values[lower]) * (k - lower)


def austin_unit_price(category):
    """Median / 25th / 75th percentile unit price for a category in Austin.

    Returns "not available" when there are fewer than MIN_PURCHASES priced
    purchases. Reusable by /get_budget_context.
    """
    conn = get_connection()
    try:
        rows = conn.cursor().execute(AUSTIN_PRICES_SQL, category, category).fetchall()
    finally:
        conn.close()

    prices = [p for p in (_to_price(row[0]) for row in rows) if p is not None]

    if len(prices) < MIN_PURCHASES:
        return NOT_AVAILABLE

    prices.sort()
    return {
        "median": round(_percentile(prices, 0.50), 2),
        "low": round(_percentile(prices, 0.25), 2),
        "high": round(_percentile(prices, 0.75), 2),
        "purchases": len(prices),
    }


@router.post("/get_unit_price")
def get_unit_price(request: UnitPriceRequest):
    category = request.category.strip() if isinstance(request.category, str) else ""
    if not category:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "category is required"},
        )

    try:
        austin = austin_unit_price(category)
    except Exception:
        log.exception("Azure SQL query failed for /get_unit_price")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "price data is unavailable right now"},
        )

    return {
        "success": True,
        "category": category,
        "unitPrice": {
            "Austin": austin,
            "Dallas": NOT_AVAILABLE,
            "Texas": NOT_AVAILABLE,
        },
    }
