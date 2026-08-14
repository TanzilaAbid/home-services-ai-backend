from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.pricing_service import estimate_price

router = APIRouter()


class PriceEstimateRequest(BaseModel):
    service_type: str = Field(..., examples=["painter"])
    room_sqft: float = Field(..., gt=0, examples=[250])
    wall_condition: str = Field(default="average", examples=["average"])
    num_rooms: int = Field(default=1, gt=0, examples=[3])


class PriceEstimateResponse(BaseModel):
    price_min: float
    price_max: float
    estimated_hours: float
    currency: str


@router.post("/price-estimate", response_model=PriceEstimateResponse)
def price_estimate(request: PriceEstimateRequest):
    try:
        result = estimate_price(
            service_type=request.service_type,
            room_sqft=request.room_sqft,
            wall_condition=request.wall_condition,
            num_rooms=request.num_rooms,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
