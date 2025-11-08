from typing import Annotated

from fastapi import Cookie, Depends

from core.exceptions.auth import InvalidCredentials
from core.protocols.repositories import (
    PriceRepositoryProtocol,
    PriceVariantRepositoryProtocol,
    UserRepositoryProtocol,
)
from core.protocols.security import SecurityProtocol
from core.schemas.users import UserOutDto
from core.services.auth import AuthService
from core.services.prices import PriceService
from depends.repositories import (
    get_price_repository,
    get_price_variant_repository,
    get_user_repository,
)
from depends.utils import get_security


async def get_auth_service(
    user_repository: Annotated[UserRepositoryProtocol, Depends(get_user_repository)],
    security: Annotated[SecurityProtocol, Depends(get_security)],
) -> AuthService:
    return AuthService(user_repository=user_repository, security=security)


async def get_current_user(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    access_token: Annotated[str | None, Cookie(alias="access_token")] = None,
) -> UserOutDto:
    if access_token is None:
        raise InvalidCredentials("Токен доступа не найден")

    return await auth_service.get_current_user(token=access_token)


async def get_price_service(
    price_repository: Annotated[PriceRepositoryProtocol, Depends(get_price_repository)],
    price_variant_repository: Annotated[
        PriceVariantRepositoryProtocol, Depends(get_price_variant_repository)
    ],
) -> PriceService:
    return PriceService(
        price_repository=price_repository,
        price_variant_repository=price_variant_repository,
    )
