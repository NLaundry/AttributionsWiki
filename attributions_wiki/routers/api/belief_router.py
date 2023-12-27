"""Belief router."""
from typing import List

from fastapi import APIRouter

from prisma.models import Belief
from prisma.types import BeliefCreateInput, BeliefUpdateInput, BeliefWhereUniqueInput

from ...db import db

router = APIRouter(
    prefix="/belief",
    tags=["belief"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_belief(belief_data: BeliefCreateInput) -> Belief:
    """Create a new belief.

    Args: belief_data: BeliefCreateInput
    Returns: Belief
    """
    new_belief: Belief = await db.belief.create(belief_data)
    return new_belief


@router.get("/get_all")
async def get_beliefs() -> List[Belief]:
    """Get all beliefs.

    Returns: List[Belief]
    """
    beliefs: List[Belief] = await db.belief.find_many()
    return beliefs


@router.get("/get/{id}")
async def get_belief_by_id(id: int) -> Belief:
    """Get a single belief by id.
    
    Args: id: int
    Returns: Belief
    """
    id_obj: BeliefWhereUniqueInput = BeliefWhereUniqueInput(id=id)
    belief: Belief = await db.belief.find_unique_or_raise(id_obj)
    return belief


@router.delete("/delete/{id}")
async def delete_belief_by_id(id: int) -> Belief | None:
    """Delete a single belief by id.
    
    Args: id: int
    Returns: Belief or None
    """
    id_obj: BeliefWhereUniqueInput = BeliefWhereUniqueInput(id=id)
    belief: Belief | None = await db.belief.delete(id_obj)
    return belief


@router.put("/update/{id}")
async def update_belief(data: BeliefUpdateInput, id: int) -> Belief | None:
    """Update a single belief by id.

    Args: data: BeliefUpdateInput, id: int
    Returns: Belief or None
    """
    id_obj: BeliefWhereUniqueInput = BeliefWhereUniqueInput(id=id)
    belief: Belief | None = await db.belief.update(data=data, where=id_obj)
    return belief
