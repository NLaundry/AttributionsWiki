"""Factor router."""
from typing import List

from fastapi import APIRouter, HTTPException

from prisma.models import Factor
from prisma.types import FactorCreateInput, FactorUpdateInput, FactorWhereUniqueInput

from ...exceptions import (
    DatabaseError,
    DeletionError,
    NotFoundError,
    UpdateError,
    ValidationError,
)
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

    Args:
        factor_data: FactorCreateInput - The data to create a new factor.

    Returns:
        Factor: The newly created factor.

    Raises:
        HTTPException: For validation or database errors.
    """
    try:
        return await create_factor(factor_data)
    except ValidationError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.get("/get_all")
async def get_factors_route() -> List[Factor]:
    """Get all factors.

    Returns:
        List[Factor]: A list of all factors.

    Raises:
        HTTPException: For database errors.
    """
    try:
        return await get_factors()
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.get("/get/{id}")
async def get_factor_by_id_route(id: int) -> Factor:
    """Get a factor by id.

    Args:
        id: int - The unique identifier for the factor.

    Returns:
        Factor: The requested factor.

    Raises:
        HTTPException: For not found or database errors.
    """
    try:
        id_obj: FactorWhereUniqueInput = {"id": id}
        return await get_factor_by_id(id_obj)
    except NotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.delete("/delete/{id}")
async def delete_factor_by_id_route(id: int) -> Factor | None:
    """Delete a factor by id.

    Args:
        id: int - The unique identifier for the factor to delete.

    Returns:
        Factor | None: The deleted factor, or None if it wasn't found.

    Raises:
        HTTPException: For deletion or database errors.
    """
    try:
        id_obj: FactorWhereUniqueInput = {"id": id}
        return await delete_factor_by_id(id_obj)
    except DeletionError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.put("/update/{id}")
async def update_factor_route(data: FactorUpdateInput, id: int) -> Factor | None:
    """Update a factor by id.

    Args:
        id: int - The unique identifier for the factor to update.
        data: FactorUpdateInput - The data to update the factor with.

    Returns:
        Factor | None: The updated factor, or None if it wasn't found.

    Raises:
        HTTPException: For update or database errors.
    """
    try:
        id_obj: FactorWhereUniqueInput = {"id": id}
        return await update_factor(id_obj=id_obj, factor_data=data)
    except UpdateError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err
