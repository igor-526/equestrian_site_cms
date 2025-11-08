from typing import Protocol
from uuid import UUID

from core.entities import PaginatedEntities, Price, PriceVariant

from .base_repository import BaseRepositoryProtocol


class PriceRepositoryProtocol(BaseRepositoryProtocol[Price], Protocol):
    async def get_all_prices(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        description: str | None = None,
        group: list[str] | None = None,
        price_gt: int | None = None,
        price_lt: int | None = None,
        sort: list[str] | None = None,
    ) -> PaginatedEntities[Price]: ...
    """Получает все цены услуг c фильтрацией."""

    async def get_by_unique(
        self, *, name: str, group: str | None
    ) -> Price | None: ...
    """Получает цену услуги по уникальному ключу."""

    async def list_groups(self) -> list[str]: ...
    """Получает все имеющиеся группы цен."""


class PriceVariantRepositoryProtocol(
    BaseRepositoryProtocol[PriceVariant], Protocol
):
    async def get_all_price_variants(
        self,
        *,
        price_ids: list[UUID] | None = None,
    ) -> list[PriceVariant]: ...
    """Получает все варианты цен услуг c фильтрацией."""

    async def get_by_unique(self, *, name: str, price_id: UUID) -> PriceVariant | None: ...
    """Получает вариант цены услуги по уникальному ключу."""