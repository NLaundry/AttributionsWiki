"""Belief router."""
from typing import List

from fastapi import APIRouter, HTTPException

from prisma.models import Belief
from prisma.types import BeliefCreateInput, BeliefUpdateInput, BeliefWhereUniqueInput

from ...exceptions import (
    DatabaseError,
    DeletionError,
    NotFoundError,
    UpdateError,
    ValidationError,
)
from ...services.belief_service import (
    create_belief,
    delete_belief_by_id,
    get_belief_by_id,
    get_beliefs,
    update_belief,
)

router = APIRouter(
    prefix="/belief",
    tags=["belief"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_belief_route(belief_data: BeliefCreateInput) -> Belief:
    """Create a new belief.

    Args:
        belief_data: BeliefCreateInput - The data to create a new belief.

    Returns:
        Belief: The newly created belief.

    Raises:
        HTTPException: For validation or database errors.
    """
    try:
        return await create_belief(belief_data)
    except ValidationError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.get("/get_all")
async def get_beliefs_route() -> List[Belief]:
    """Get all beliefs.

    Returns:
        List[Belief]: A list of all beliefs.

    Raises:
        HTTPException: For database errors.
    """
    try:
        return await get_beliefs()
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.get("/get/{id}")
async def get_belief_by_id_route(id: int) -> Belief:
    """Get a belief by id.

    Args:
        id: int - The unique identifier for the belief.

    Returns:
        Belief: The requested belief.

    Raises:
        HTTPException: For not found or database errors.
    """
    try:
        id_obj: BeliefWhereUniqueInput = {"id": id}
        return await get_belief_by_id(id_obj)
    except NotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.delete("/delete/{id}")
async def delete_belief_by_id_route(id: int) -> Belief | None:
    """Delete a belief by id.

    Args:
        id: int - The unique identifier for the belief to delete.

    Returns:
        Belief | None: The deleted belief, or None if it wasn't found.

    Raises:
        HTTPException: For deletion or database errors.
    """
    try:
        id_obj: BeliefWhereUniqueInput = {"id": id}
        return await delete_belief_by_id(id_obj)
    except DeletionError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router.put("/update/{id}")
async def update_belief_route(data: BeliefUpdateInput, id: int) -> Belief | None:
    """Update a belief by id.

    Args:
        id: int - The unique identifier for the belief to update.
        data: BeliefUpdateInput - The data to update the belief with.

    Returns:
        Belief | None: The updated belief, or None if it wasn't found.

    Raises:
        HTTPException: For update or database errors.
    """
    try:
        id_obj: BeliefWhereUniqueInput = {"id": id}
        return await update_belief(id_obj=id_obj, belief_data=data)
    except UpdateError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except DatabaseError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err
