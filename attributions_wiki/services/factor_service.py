"""Factor router."""
from typing import List

from prisma.models import Factor
from prisma.types import FactorCreateInput, FactorUpdateInput, FactorWhereUniqueInput

from ..db import db


async def create_factor(factor_data: FactorCreateInput) -> Factor:
    """Create a new factor.

    Args: factor_data: FactorCreateInput
    Returns: Factor
    """
    new_factor: Factor = await db.factor.create(factor_data)
    return new_factor


async def get_factors() -> List[Factor]:
    """Get all factors.

    Returns: List[Factor]
    """
    factors: List[Factor] = await db.factor.find_many()
    return factors


async def get_factor_by_id(id_obj: FactorWhereUniqueInput) -> Factor:
    """Get a factor by id.

    Returns: Factor
    """
    factor: Factor = await db.factor.find_unique_or_raise(id_obj)  # type: ignore
    return factor


async def delete_factor_by_id(id_obj: FactorWhereUniqueInput) -> Factor | None:
    """Delete a factor by id.

    Returns: Factor
    """
    factor: Factor | None = await db.factor.delete(id_obj)  # type: ignore
    return factor


async def update_factor(
    id_obj: FactorWhereUniqueInput, factor_data: FactorUpdateInput
) -> Factor:
    """Update a factor by id.

    Returns: Factor
    """
    factor: Factor = await db.factor.update(where=id_obj, data=factor_data)  # type: ignore
    return factor
