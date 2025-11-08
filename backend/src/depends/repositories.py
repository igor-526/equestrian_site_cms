from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.protocols.repositories import (
    UserRepositoryProtocol,
    PriceRepositoryProtocol,
    PriceVariantRepositoryProtocol,
)
from depends.utils import get_session
from repositories import (
    UserRepository,
    PriceRepository,
    PriceVariantRepository,
)


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepositoryProtocol:
    return UserRepository(session=session)


async def get_price_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PriceRepositoryProtocol:
    return PriceRepository(session=session)


async def get_price_variant_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PriceVariantRepositoryProtocol:
    return PriceVariantRepository(session=session)
