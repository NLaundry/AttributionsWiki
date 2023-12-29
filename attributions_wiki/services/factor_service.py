"""Factor Service."""
from typing import List

from prisma.errors import MissingRequiredValueError, PrismaError, RecordNotFoundError
from prisma.models import Factor
from prisma.types import FactorCreateInput, FactorUpdateInput, FactorWhereUniqueInput

from ..db import db
from ..exceptions import (
    DatabaseError,
    DeletionError,
    NotFoundError,
    UpdateError,
    ValidationError,
)


async def create_factor(factor_data: FactorCreateInput) -> Factor:
    """Create a new factor.

    Args:
        factor_data: FactorCreateInput - The data to create a new factor.

    Returns:
        Factor - The newly created factor.

    Raises:
        ValidationError: If the factor creation fails due to missing required values.
        DatabaseError: If there is a more general database issue during factor creation.
    """
    try:
        new_factor: Factor = await db.factor.create(factor_data)
    except MissingRequiredValueError as err:
        raise ValidationError("Missing required value") from err
    except PrismaError as err:
        raise DatabaseError("Unknown issue during factor creation") from err
    else:
        return new_factor


async def get_factors() -> List[Factor]:
    """Get all factors.

    Returns:
        List[Factor]: A list of all factors.

    Raises:
        DatabaseError: If there is an issue communicating with the database.
    """
    try:
        factors: List[Factor] = await db.factor.find_many()
    except PrismaError as err:
        raise DatabaseError("Issue retrieving all factors") from err
    else:
        return factors


async def get_factor_by_id(id_obj: FactorWhereUniqueInput) -> Factor:
    """Get a factor by its unique ID.

    Args:
        id_obj: FactorWhereUniqueInput - The unique identifier for the factor.

    Returns:
        Factor: The requested factor.

    Raises:
        NotFoundError: If no factor with the given ID is found.
        DatabaseError: If there is an issue communicating with the database.
    """
    try:
        factor: Factor = await db.factor.find_unique_or_raise(id_obj)  # type: ignore
    except RecordNotFoundError as err:
        raise NotFoundError(f"Factor with ID: {id_obj} not found") from err
    except PrismaError as err:
        raise DatabaseError("Issue retrieving factor by ID") from err
    else:
        return factor


async def delete_factor_by_id(id_obj: FactorWhereUniqueInput) -> Factor | None:
    """Delete a factor by its unique ID.

    Args:
        id_obj: FactorWhereUniqueInput - The unique identifier for the factor.

    Returns:
        Factor | None: The deleted factor, or None if it wasn't found.

    Raises:
        DeletionError: If the factor is not found and Deletion Fails
        ValidationError: If the factor deletion fails due to missing required values.
        DatabaseError: If there is an issue communicating with the database.
    """
    try:
        factor: Factor | None = await db.factor.delete(id_obj)  # type: ignore
        if factor is None:
            raise DeletionError("Factor Not Found - Deletion Failed")
    except MissingRequiredValueError as err:
        raise ValidationError("Missing required value") from err
    except PrismaError as err:
        raise DatabaseError("Issue during factor deletion") from err
    else:
        return factor


async def update_factor(
    id_obj: FactorWhereUniqueInput, factor_data: FactorUpdateInput
) -> Factor:
    """Update a factor by its unique ID.

    Args:
        id_obj: FactorWhereUniqueInput - The unique identifier for the factor.
        factor_data: FactorUpdateInput - The data to update the factor with.

    Returns:
        Factor: The updated factor.

    Raises:
        UpdateError: If the factor cannot be updated or is not found.
        DatabaseError: If there is an issue communicating with the database.
    """
    if not factor_data:
        raise MissingRequiredValueError("No data provided for factor update")
    if not id_obj:
        raise MissingRequiredValueError("No ID provided for factor update")

    try:
        factor: Factor | None = await db.factor.update(where=id_obj, data=factor_data)  
        if factor is None:
            raise UpdateError("Factor update failed or factor not found")
    except PrismaError as err:
        raise DatabaseError("Issue during factor update") from err
    else:
        return factor
