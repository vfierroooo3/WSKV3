"""POST /get_budget_context — matches requested items to Austin categories and estimates project costs.

Utilizes the austin_unit_price function to fetch historical pricing. 
Currently relies on exact-match for categories until the LLM microservice is integrated.
"""
import logging
from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

# Import the existing function and constant from your unit_price module
from unit_price import austin_unit_price, NOT_AVAILABLE

router = APIRouter()
log = logging.getLogger(__name__)


class BudgetItemRequest(BaseModel):
    description: str
    quantity: int = Field(gt=0)


class BudgetContextRequest(BaseModel):
    orgId: str
    budget: float
    items: List[BudgetItemRequest]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "orgId": "AUS",
                "budget": 20000.0,
                "items": [
                    {"description": "LIGHTS, EMERGENCY", "quantity": 20}
                ]
            }
        }
    )


def match_description_to_category(description: str):
    """
    Placeholder matcher until external LLM microservice is connected.
    Currently accepts exact category names or commodity codes.
    Returns: (matched_category, confidence)
    """
    cleaned = description.strip()
    if cleaned:
        return cleaned, 1.0
    return None, 0.0


@router.post("/get_budget_context")
def get_budget_context(request: BudgetContextRequest):
    if not request.items:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "items list cannot be empty"},
        )

    try:
        item_results = []
        total_low = 0.0
        total_typical = 0.0
        total_high = 0.0
        has_valid_estimates = False
        
        unpriced_items_count = 0

        for item in request.items:
            desc = item.description.strip()
            matched_category, confidence = match_description_to_category(desc)

            unit_price = NOT_AVAILABLE
            est_cost = NOT_AVAILABLE

            if matched_category:
                price_data = austin_unit_price(matched_category)

                if isinstance(price_data, dict):
                    unit_price = price_data
                    
                    e_low = round(price_data["low"] * item.quantity, 2)
                    e_typ = round(price_data["median"] * item.quantity, 2)
                    e_high = round(price_data["high"] * item.quantity, 2)
                    
                    est_cost = {
                        "low": e_low,
                        "typical": e_typ,
                        "high": e_high
                    }

                    total_low += e_low
                    total_typical += e_typ
                    total_high += e_high
                    has_valid_estimates = True
                else:
                    unpriced_items_count += 1
            else:
                unpriced_items_count += 1

            item_results.append({
                "description": desc,
                "quantity": item.quantity,
                "matchedCategory": matched_category if unit_price != NOT_AVAILABLE else None,
                "confidence": confidence if unit_price != NOT_AVAILABLE else 0.0,
                "unitPrice": unit_price,
                "estimatedCost": est_cost
            })

        if has_valid_estimates:
            total_estimate = {
                "low": round(total_low, 2),
                "typical": round(total_typical, 2),
                "high": round(total_high, 2)
            }
            within_budget = (total_typical <= request.budget) if unpriced_items_count == 0 else None
        else:
            total_estimate = NOT_AVAILABLE
            within_budget = None

        return {
            "success": True,
            "orgId": request.orgId,
            "budget": request.budget,
            "items": item_results,
            "totalEstimate": total_estimate,
            "withinBudget": within_budget,
            "unpricedItems": unpriced_items_count
        }

    except Exception:
        log.exception("Failed to calculate budget context for /get_budget_context")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "budget context is unavailable right now"},
        )