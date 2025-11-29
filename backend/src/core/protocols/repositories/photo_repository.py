from typing import Literal, Protocol

from core.entities.photos import Photo

from .base_repository import BaseRepositoryProtocol


class PhotoRepositoryProtocol(BaseRepositoryProtocol[Photo], Protocol):
    async def find_by_name(self, name: str) -> Photo | None: ...
    async def get_filtered(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        sort: list[Literal["name", "description", "-name", "-description"]] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> tuple[list[Photo], int]: ...



