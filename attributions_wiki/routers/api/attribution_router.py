"""Attribution router."""
from typing import List

from fastapi import APIRouter, HTTPException

from prisma.models import Attribution
from prisma.types import (
    AttributionCreateInput,
    AttributionUpdateInput,
    AttributionWhereUniqueInput,
)

from ...db import db

router = APIRouter(
    prefix="/attribution",
    tags=["attribution"],
    responses={404: {"description": "Attribution not found"}},
)

@router.post("/create")
async def create_attribution(attribution_data: AttributionCreateInput) -> Attribution:
    """Create a new attribution.

    Args: attribution_data: AttributionCreateInput
    Returns: Attribution
    """
    try:
        new_attribution: Attribution = await db.attribution.create(attribution_data)
        return new_attribution
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_all")
async def get_attributions() -> List[Attribution]:
    """Get all attributions.

    Returns: List[Attribution]
    """
    try:
        attributions: List[Attribution] = await db.attribution.find_many()
        return attributions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@router.get("/get/{id}")
async def get_attribution_by_id(id: int) -> Attribution:
    """Get attribution defined by a given id.
    
    Args: id: int
    Returns: Attribution
    """
    id_obj: AttributionWhereUniqueInput = AttributionWhereUniqueInput(id=id)
    attribution: Attribution | None = await db.attribution.find_unique(id_obj)
    if not attribution:
        raise HTTPException(status_code=404, detail="Attribution not found")
    return attribution


@router.delete("/delete/{id}")
async def delete_attribution_by_id(id: int) -> Attribution | None:
    """Delete attribution defined by a given id.

    Args: id: int
    Returns: Attribution or None
    """
    id_obj: AttributionWhereUniqueInput = AttributionWhereUniqueInput(id=id)
    attribution: Attribution | None = await db.attribution.delete(id_obj)
    if not attribution:
        raise HTTPException(status_code=404, detail="Attribution not found")


@router.put("/update/{id}")
async def update_attribution(
    data: AttributionUpdateInput, id: int
) -> Attribution | None:
    """
    Update attribution defined by a given id.

    Args: data: AttributionUpdateInput, id: int
    Returns: Attribution or None
    """
    id_obj: AttributionWhereUniqueInput = AttributionWhereUniqueInput(id=id)
    try:
        attribution: Attribution | None = await db.attribution.update(data=data, where=id_obj)
        if not attribution:
            raise HTTPException(status_code=404, detail="Attribution not found")
        return attribution
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))