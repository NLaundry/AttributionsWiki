"""Factor router."""
from typing import List

from fastapi import APIRouter

from prisma.models import Factor
from prisma.types import FactorCreateInput, FactorUpdateInput, FactorWhereUniqueInput

from ...db import db

router = APIRouter(
    prefix="/factor",
    tags=["factor"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_factor(factor_data: FactorCreateInput) -> Factor:
    """Create a new factor.

    Args: factor_data: FactorCreateInput
    Returns: Factor
    """
    new_factor: Factor = await db.factor.create(factor_data)
    return new_factor


@router.get("/get_all")
async def get_factors() -> List[Factor]:
    """Get all factors.

    Returns: List[Factor]
    """
    factors: List[Factor] = await db.factor.find_many()
    return factors


@router.get("/get/{id}")
async def get_factor_by_id(id: int) -> Factor:
    id_obj: FactorWhereUniqueInput = FactorWhereUniqueInput(id=id)  # type: ignore
    factor: Factor = await db.factor.find_unique_or_raise(id_obj)  # type: ignore
    return factor


@router.delete("/delete/{id}")
async def delete_factor_by_id(id: int) -> Factor | None:
    id_obj: FactorWhereUniqueInput = FactorWhereUniqueInput(id=id)  # type: ignore
    factor: Factor | None = await db.factor.delete(id_obj)  # type: ignore
    return factor


@router.put("/update/{id}")
async def update_factor(data: FactorUpdateInput, id: int) -> Factor | None:
    id_obj: FactorWhereUniqueInput = FactorWhereUniqueInput(id=id)  # type: ignore
    factor: Factor | None = await db.factor.update(data=data, where=id_obj)  # type: ignore
    return factor
