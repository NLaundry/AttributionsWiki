"""Factor router."""
from typing import List

from fastapi import APIRouter, HTTPException

from prisma.models import Factor
from prisma.types import FactorCreateInput, FactorUpdateInput, FactorWhereUniqueInput

from ...db import db

router = APIRouter(
    prefix="/factor",
    tags=["factor"],
    responses={404: {"description": "Factor not found"}},
)


@router.post("/create")
async def create_factor(factor_data: FactorCreateInput) -> Factor:
    """Create a new factor.

    Args: factor_data: FactorCreateInput
    Returns: Factor
    """
    try:
        new_factor: Factor = await db.factor.create(factor_data)
        return new_factor
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_all")
async def get_factors() -> List[Factor]:
    """Get all factors.

    Returns: List[Factor]
    """
    try:
        factors: List[Factor] = await db.factor.find_many()
        return factors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/{id}")
async def get_factor_by_id(id: int) -> Factor:
    """ Get a single factor by id.

    Args: id: int
    Returns: Factor
    """
    id_obj: FactorWhereUniqueInput = FactorWhereUniqueInput(id=id)  # type: ignore
    factor: Factor = await db.factor.find_unique_or_raise(id_obj)  # type: ignore
    if not factor:
        raise HTTPException(status_code=404, detail="Factor not found")
    return factor


@router.delete("/delete/{id}")
async def delete_factor_by_id(id: int) -> Factor | None:
    """Delete a single factor by id.

    Args: id: int
    Returns: Factor or None
    """
    id_obj: FactorWhereUniqueInput = FactorWhereUniqueInput(id=id)  # type: ignore
    factor: Factor | None = await db.factor.delete(id_obj)  # type: ignore
    if not factor:
        raise HTTPException(status_code=404, detail="Factor not found")
    return factor


@router.put("/update/{id}")
async def update_factor(data: FactorUpdateInput, id: int) -> Factor | None:
    """Update a single factor by id.

    Args: data: FactorUpdateInput, id: int
    Returns: Factor or None
    """
    id_obj: FactorWhereUniqueInput = FactorWhereUniqueInput(id=id)  # type: ignore
    try:

        factor: Factor | None = await db.factor.update(data=data, where=id_obj)  # type: ignore
        if not factor:
            raise HTTPException(status_code=404, detail="Factor not found")
        return factor
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
