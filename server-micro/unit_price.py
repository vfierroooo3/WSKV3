"""POST /get_unit_price — what governments typically pay per unit for a category.

Only the Austin data has quantities and unit prices, so Dallas and Texas
always come back as "not available" (see the Projects Group API Contract).
"""
import math
import os
import re
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from database import client

router = APIRouter()

# Ranya's Atlas database; override with HARDWARE_DB in .env if it moves.
hardware_db = client[os.environ.get("HARDWARE_DB", "apad-hardware")]
austin_collection = hardware_db["austin"]

# Field names differ depending on how the data was loaded (raw SODA API
# vs. a cleaned/categorized load), so check each known spelling.
CATEGORY_FIELDS = ["category", "commodity_description", "Commodity Description"]
PRICE_FIELDS = ["unit_price", "Unit Price", "unitPrice"]

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
    match = {"$regex": f"^{re.escape(category)}$", "$options": "i"}
    query = {"$or": [{field: match} for field in CATEGORY_FIELDS]}
    projection = {field: 1 for field in PRICE_FIELDS}
    projection["_id"] = 0

    prices = []
    for doc in austin_collection.find(query, projection):
        for field in PRICE_FIELDS:
            price = _to_price(doc.get(field))
            if price is not None:
                prices.append(price)
                break

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

    return {
        "success": True,
        "category": category,
        "unitPrice": {
            "Austin": austin_unit_price(category),
            "Dallas": NOT_AVAILABLE,
            "Texas": NOT_AVAILABLE,
        },
    }
