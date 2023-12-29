"""Belief service."""
from typing import List

from prisma.errors import MissingRequiredValueError, PrismaError, RecordNotFoundError
from prisma.models import Belief
from prisma.types import BeliefCreateInput, BeliefUpdateInput, BeliefWhereUniqueInput

from ..db import db
from ..exceptions import (
    DatabaseError,
    DeletionError,
    NotFoundError,
    UpdateError,
    ValidationError,
)


async def create_belief(belief_data: BeliefCreateInput) -> Belief:
    """Create a new belief.

    Args:
        belief_data: BeliefCreateInput - The data to create a new belief.

    Returns:
        Belief - The newly created belief.

    Raises:
        ValidationError: If the belief creation fails due to missing required values.
        DatabaseError: If there is a more general database issue during belief creation.
    """
    try:
        new_belief: Belief = await db.belief.create(belief_data)
    except MissingRequiredValueError as err:
        raise ValidationError("Missing required value") from err
    except PrismaError as err:
        raise DatabaseError("Unknown issue during belief creation") from err
    else:
        return new_belief


async def get_beliefs() -> List[Belief]:
    """Get all beliefs.

    Returns:
        List[Belief]: A list of all beliefs.

    Raises:
        DatabaseError: If there is an issue communicating with the database.
    """
    try:
        beliefs: List[Belief] = await db.belief.find_many()
    except PrismaError as err:
        raise DatabaseError("Issue retrieving all beliefs") from err
    else:
        return beliefs


async def get_belief_by_id(id_obj: BeliefWhereUniqueInput) -> Belief:
    """Get a belief by its unique ID.

    Args:
        id_obj: BeliefWhereUniqueInput - The unique identifier for the belief.

    Returns:
        Belief: The requested belief.

    Raises:
        NotFoundError: If no belief with the given ID is found.
        DatabaseError: If there is an issue communicating with the database.
    """
    try:
        belief: Belief = await db.belief.find_unique_or_raise(id_obj)  # type: ignore
    except RecordNotFoundError as err:
        raise NotFoundError(f"Belief with ID: {id_obj} not found") from err
    except PrismaError as err:
        raise DatabaseError("Issue retrieving belief by ID") from err
    else:
        return belief


async def delete_belief_by_id(id_obj: BeliefWhereUniqueInput) -> Belief | None:
    """Delete a belief by its unique ID.

    Args:
        id_obj: BeliefWhereUniqueInput - The unique identifier for the belief.

    Returns:
        Belief | None: The deleted belief, or None if it wasn't found.

    Raises:
        DeletionError: If the belief is not found and Deletion Fails
        ValidationError: If the belief deletion fails due to missing required values.
        DatabaseError: If there is an issue communicating with the database.
    """
    try:
        belief: Belief | None = await db.belief.delete(id_obj)  # type: ignore
        if belief is None:
            raise DeletionError("Belief Not Found - Deletion Failed")
    except MissingRequiredValueError as err:
        raise ValidationError("Missing required value") from err
    except PrismaError as err:
        raise DatabaseError("Issue during belief deletion") from err
    else:
        return belief


async def update_belief(
    id_obj: BeliefWhereUniqueInput, belief_data: BeliefUpdateInput
) -> Belief:
    """Update a belief by its unique ID.

    Args:
        id_obj: BeliefWhereUniqueInput - The unique identifier for the belief.
        belief_data: BeliefUpdateInput - The data to update the belief with.

    Returns:
        Belief: The updated belief.

    Raises:
        UpdateError: If the belief cannot be updated or is not found.
        DatabaseError: If there is an issue communicating with the database.
    """
    if not belief_data:
        raise MissingRequiredValueError("No data provided for belief update")
    if not id_obj:
        raise MissingRequiredValueError("No ID provided for belief update")

    try:
        belief: Belief | None = await db.belief.update(where=id_obj, data=belief_data)  
        if belief is None:
            raise UpdateError("Belief update failed or belief not found")
    except PrismaError as err:
        raise DatabaseError("Issue during belief update") from err
    else:
        return belief
