"""Attribution service."""
from typing import List

from prisma.errors import MissingRequiredValueError, PrismaError, RecordNotFoundError
from prisma.models import Attribution
from prisma.types import (
    AttributionCreateInput,
    AttributionUpdateInput,
    AttributionWhereUniqueInput,
)

from ..db import db
from ..exceptions import (
    DatabaseError,
    DeletionError,
    NotFoundError,
    UpdateError,
    ValidationError,
)


async def create_attribution(attribution_data: AttributionCreateInput) -> Attribution:
    """Create a new attribution.

    Args:
        attribution_data: AttributionCreateInput - The data to create a new attribution.

    Returns:
        Attribution - The newly created attribution.

    Raises:
        ValidationError: If the attribution creation fails due to missing required values.
        DatabaseError: If there is a more general database issue during attribution creation.
    """
    try:
        new_attribution: Attribution = await db.attribution.create(attribution_data)
    except MissingRequiredValueError as err:
        raise ValidationError("Missing required value") from err
    except PrismaError as err:
        raise DatabaseError("Unknown issue during attribution creation") from err
    else:
        return new_attribution


async def get_attributions() -> List[Attribution]:
    """Get all attributions.

    Returns:
        List[Attribution]: A list of all attributions.

    Raises:
        DatabaseError: If there is an issue communicating with the database.
    """
    try:
        attributions: List[Attribution] = await db.attribution.find_many()
    except PrismaError as err:
        raise DatabaseError("Issue retrieving all attributions") from err
    else:
        return attributions


async def get_attribution_by_id(id_obj: AttributionWhereUniqueInput) -> Attribution:
    """Get a attribution by its unique ID.

    Args:
        id_obj: AttributionWhereUniqueInput - The unique identifier for the attribution.

    Returns:
        Attribution: The requested attribution.

    Raises:
        NotFoundError: If no attribution with the given ID is found.
        DatabaseError: If there is an issue communicating with the database.
    """
    try:
        attribution: Attribution = await db.attribution.find_unique_or_raise(id_obj)  # type: ignore
    except RecordNotFoundError as err:
        raise NotFoundError(f"Attribution with ID: {id_obj} not found") from err
    except PrismaError as err:
        raise DatabaseError("Issue retrieving attribution by ID") from err
    else:
        return attribution


async def delete_attribution_by_id(id_obj: AttributionWhereUniqueInput) -> Attribution | None:
    """Delete a attribution by its unique ID.

    Args:
        id_obj: AttributionWhereUniqueInput - The unique identifier for the attribution.

    Returns:
        Attribution | None: The deleted attribution, or None if it wasn't found.

    Raises:
        DeletionError: If the attribution is not found and Deletion Fails
        ValidationError: If the attribution deletion fails due to missing required values.
        DatabaseError: If there is an issue communicating with the database.
    """
    try:
        attribution: Attribution | None = await db.attribution.delete(id_obj)  # type: ignore
        if attribution is None:
            raise DeletionError("Attribution Not Found - Deletion Failed")
    except MissingRequiredValueError as err:
        raise ValidationError("Missing required value") from err
    except PrismaError as err:
        raise DatabaseError("Issue during attribution deletion") from err
    else:
        return attribution


async def update_attribution(
    id_obj: AttributionWhereUniqueInput, attribution_data: AttributionUpdateInput
) -> Attribution:
    """Update a attribution by its unique ID.

    Args:
        id_obj: AttributionWhereUniqueInput - The unique identifier for the attribution.
        attribution_data: AttributionUpdateInput - The data to update the attribution with.

    Returns:
        Attribution: The updated attribution.

    Raises:
        UpdateError: If the attribution cannot be updated or is not found.
        DatabaseError: If there is an issue communicating with the database.
    """
    if not attribution_data:
        raise MissingRequiredValueError("No data provided for attribution update")
    if not id_obj:
        raise MissingRequiredValueError("No ID provided for attribution update")

    try:
        attribution: Attribution | None = await db.attribution.update(where=id_obj, data=attribution_data)  
        if attribution is None:
            raise UpdateError("Attribution update failed or attribution not found")
    except PrismaError as err:
        raise DatabaseError("Issue during attribution update") from err
    else:
        return attribution
