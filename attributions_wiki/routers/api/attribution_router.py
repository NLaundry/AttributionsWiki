"""Attribution router."""
from typing import List

from fastapi import APIRouter

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
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_attribution(attribution_data: AttributionCreateInput) -> Attribution:
    """Create a new attribution.

    Args: attribution_data: AttributionCreateInput
    Returns: Attribution
    """
    new_attribution: Attribution = await db.attribution.create(attribution_data)
    return new_attribution


@router.get("/get_all")
async def get_attributions() -> List[Attribution]:
    """Get all attributions.

    Returns: List[Attribution]
    """
    attributions: List[Attribution] = await db.attribution.find_many()
    return attributions


@router.get("/get/{id}")
async def get_attribution_by_id(id: int) -> Attribution:
    id_obj: AttributionWhereUniqueInput = AttributionWhereUniqueInput(id=id)
    attribution: Attribution = await db.attribution.find_unique_or_raise(id_obj)
    return attribution


@router.delete("/delete/{id}")
async def delete_attribution_by_id(id: int) -> Attribution | None:
    id_obj: AttributionWhereUniqueInput = AttributionWhereUniqueInput(id=id)
    attribution: Attribution | None = await db.attribution.delete(id_obj)
    return attribution


@router.put("/update/{id}")
async def update_attribution(
    data: AttributionUpdateInput, id: int
) -> Attribution | None:
    id_obj: AttributionWhereUniqueInput = AttributionWhereUniqueInput(id=id)
    attribution: Attribution | None = await db.attribution.update(
        data=data, where=id_obj
    )
    return attribution
