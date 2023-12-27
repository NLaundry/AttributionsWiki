"""Belief router."""
from typing import List

from fastapi import APIRouter, HTTPException

from prisma.models import Belief
from prisma.types import BeliefCreateInput, BeliefUpdateInput, BeliefWhereUniqueInput

from ...db import db

router = APIRouter(
    prefix="/belief",
    tags=["belief"],
    responses={404: {"description": "Belief not found"}},
)


@router.post("/create")
async def create_belief(belief_data: BeliefCreateInput) -> Belief:
    """Create a new belief.

    Args: belief_data: BeliefCreateInput
    Returns: Belief
    """
    try:
        new_belief: Belief = await db.belief.create(belief_data)
        return new_belief
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_all")
async def get_beliefs() -> List[Belief]:
    """Get all beliefs.

    Returns: List[Belief]
    """
    try:
        beliefs: List[Belief] = await db.belief.find_many()
        return beliefs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/{id}")
async def get_belief_by_id(id: int) -> Belief:
    """Get a single belief by id.
    
    Args: id: int
    Returns: Belief
    """
    id_obj: BeliefWhereUniqueInput = BeliefWhereUniqueInput(id=id)
    belief: Belief = await db.belief.find_unique_or_raise(id_obj)
    if not belief:
        raise HTTPException(status_code=404, detail="Belief not found")
    return belief


@router.delete("/delete/{id}")
async def delete_belief_by_id(id: int) -> Belief | None:
    """Delete a single belief by id.
    
    Args: id: int
    Returns: Belief or None
    """
    id_obj: BeliefWhereUniqueInput = BeliefWhereUniqueInput(id=id)
    belief: Belief | None = await db.belief.delete(id_obj)
    if not belief:
        raise HTTPException(status_code=404, detail="Belief not found")
    return belief


@router.put("/update/{id}")
async def update_belief(data: BeliefUpdateInput, id: int) -> Belief | None:
    """Update a single belief by id.

    Args: data: BeliefUpdateInput, id: int
    Returns: Belief or None
    """
    id_obj: BeliefWhereUniqueInput = BeliefWhereUniqueInput(id=id)
    try:
        belief: Belief | None = await db.belief.update(data=data, where=id_obj)
        if not belief:
            raise HTTPException(status_code=404, detail="Belief not found")
        return belief
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
