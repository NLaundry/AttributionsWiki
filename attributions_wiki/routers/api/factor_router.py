"""Factor router."""
from typing import List

from fastapi import APIRouter

from prisma.models import Factor
from prisma.types import FactorCreateInput, FactorUpdateInput, FactorWhereUniqueInput

from ...services.factor_service import (
    create_factor,
    delete_factor_by_id,
    get_factor_by_id,
    get_factors,
    update_factor,
)

router = APIRouter(
    prefix="/factor",
    tags=["factor"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_factor_route(factor_data: FactorCreateInput) -> Factor:
    """Create a new factor.

    Args: factor_data: FactorCreateInput
    Returns: Factor
    """
    new_factor: Factor = await create_factor(factor_data)
    return new_factor


@router.get("/get_all")
async def get_factors_route() -> List[Factor]:
    """Get all factors.

    Returns: List[Factor]
    """
    factors: List[Factor] = await get_factors()
    return factors


@router.get("/get/{id}")
async def get_factor_by_id_route(id: int) -> Factor:
    """Get a factor by id.

    Returns: Factor
    """
    id_obj: FactorWhereUniqueInput = {"id": id}
    factor: Factor = await get_factor_by_id(id_obj)
    return factor


@router.delete("/delete/{id}")
async def delete_factor_by_id_route(id: int) -> Factor | None:
    """Delete a factor by id.

    Returns: Factor
    """
    id_obj: FactorWhereUniqueInput = {"id": id}
    factor: Factor | None = await delete_factor_by_id(id_obj)
    return factor


@router.put("/update/{id}")
async def update_factor_route(data: FactorUpdateInput, id: int) -> Factor | None:
    """Update a factor by id.

    Returns: Factor
    """
    id_obj: FactorWhereUniqueInput = {"id": id}
    factor: Factor | None = await update_factor(id_obj=id_obj, factor_data=data)
    return factor
