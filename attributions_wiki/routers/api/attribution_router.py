"""Attribution router."""
from typing import List

from fastapi import APIRouter, HTTPException

from prisma.models import Attribution
from prisma.types import (
    AttributionCreateInput,
    AttributionUpdateInput,
    AttributionWhereUniqueInput,
)

from ...exceptions import (
    DatabaseError,
    DeletionError,
    NotFoundError,
    UpdateError,
    ValidationError,
)
from ...services.attribution_service import (
    create_attribution,
    delete_attribution_by_id,
    get_attribution_by_id,
    get_attributions,
    update_attribution,
)

router = APIRouter(
    prefix="/attribution",
    tags=["attribution"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_attribution_route(attribution_data: AttributionCreateInput) -> Attribution:
    """Create a new attribution.

    Args:
        attribution_data: AttributionCreateInput - The data to create a new attribution.

    Returns:
        Attribution: The newly created attribution.

    Raises:
        HTTPException: For validation or database errors.
    """
    try:
        return await create_attribution(attribution_data)
    except ValidationError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.get("/get_all")
async def get_attributions_route() -> List[Attribution]:
    """Get all attributions.

    Returns:
        List[Attribution]: A list of all attributions.

    Raises:
        HTTPException: For database errors.
    """
    try:
        return await get_attributions()
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.get("/get/{id}")
async def get_attribution_by_id_route(id: int) -> Attribution:
    """Get a attribution by id.

    Args:
        id: int - The unique identifier for the attribution.

    Returns:
        Attribution: The requested attribution.

    Raises:
        HTTPException: For not found or database errors.
    """
    try:
        id_obj: AttributionWhereUniqueInput = {"id": id}
        return await get_attribution_by_id(id_obj)
    except NotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.delete("/delete/{id}")
async def delete_attribution_by_id_route(id: int) -> Attribution | None:
    """Delete a attribution by id.

    Args:
        id: int - The unique identifier for the attribution to delete.

    Returns:
        Attribution | None: The deleted attribution, or None if it wasn't found.

    Raises:
        HTTPException: For deletion or database errors.
    """
    try:
        id_obj: AttributionWhereUniqueInput = {"id": id}
        return await delete_attribution_by_id(id_obj)
    except DeletionError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.put("/update/{id}")
async def update_attribution_route(data: AttributionUpdateInput, id: int) -> Attribution | None:
    """Update a attribution by id.

    Args:
        id: int - The unique identifier for the attribution to update.
        data: AttributionUpdateInput - The data to update the attribution with.

    Returns:
        Attribution | None: The updated attribution, or None if it wasn't found.

    Raises:
        HTTPException: For update or database errors.
    """
    try:
        id_obj: AttributionWhereUniqueInput = {"id": id}
        return await update_attribution(id_obj=id_obj, attribution_data=data)
    except UpdateError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err
