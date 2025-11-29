from typing import Literal
from uuid import UUID

from sqlalchemy import Table, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.entities.photos import Photo
from models.photos import photos

from .abstract_repository import AbstractRepository


class PhotoRepository(AbstractRepository[Photo]):
    table: Table = photos
    entity = Photo

    async def find_by_name(self, name: str) -> Photo | None:
        """Проверить существование name."""
        stmt = select(self.table).where(self.table.c.name == name)
        row = await self.session.execute(stmt)
        mapping = row.mappings().first()
        if mapping is None:
            return None
        return self.entity.model_validate(dict(mapping))

    async def get_filtered(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        sort: list[Literal["name", "description", "-name", "-description"]] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> tuple[list[Photo], int]:
        """Получить отфильтрованный список с подсчётом общего количества."""
        stmt = select(self.table)
        count_stmt = select(func.count()).select_from(self.table)

        conditions = []
        if name:
            conditions.append(self.table.c.name.ilike(f"%{name}%"))
        if description:
            conditions.append(self.table.c.description.ilike(f"%{description}%"))

        if conditions:
            where_clause = or_(*conditions)
            stmt = stmt.where(where_clause)
            count_stmt = count_stmt.where(where_clause)

        # Сортировка
        if sort:
            order_by_clauses = []
            for field in sort:
                if field.startswith("-"):
                    order_by_clauses.append(self.table.c[field[1:]].desc())
                else:
                    order_by_clauses.append(self.table.c[field].asc())
            stmt = stmt.order_by(*order_by_clauses)

        # Пагинация
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)

        rows = await self.session.execute(stmt)
        entities = [self.entity.model_validate(dict(row)) for row in rows.mappings().all()]

        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar() or 0

        return entities, total



