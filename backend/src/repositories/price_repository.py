from uuid import UUID

from sqlalchemy import Table, and_, func, or_, select

from core.entities import PaginatedEntities, Price, PriceVariant
from models.prices import price_variants, prices

from .abstract_repository import AbstractRepository


class PriceRepository(AbstractRepository[Price]):
    table: Table = prices
    entity = Price

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
    ) -> PaginatedEntities[Price]:
        conditions = []
        if name:
            conditions.append(self.table.c.name.ilike(f"%{name}%"))
        if description:
            conditions.append(self.table.c.description.ilike(f"%{description}%"))
        if group:
            group_column = getattr(self.table.c, "group")
            non_null_groups = [value for value in group if value is not None]
            condition = None
            if non_null_groups:
                condition = group_column.in_(non_null_groups)
            if any(value is None for value in group):
                null_condition = group_column.is_(None)
                condition = (
                    null_condition
                    if condition is None
                    else or_(condition, null_condition)
                )
            if condition is not None:
                conditions.append(condition)
        if price_gt is not None:
            conditions.append(self.table.c.price > price_gt)
        if price_lt is not None:
            conditions.append(self.table.c.price < price_lt)

        stmt = select(self.table)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        count_stmt = select(func.count(self.table.c.id)).select_from(self.table)
        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))
        total_result = await self.session.execute(count_stmt)
        total = int(total_result.scalar_one() or 0)

        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        if sort:
            order_clauses = []
            for field in sort:
                descending = field.startswith("-")
                field_name = field[1:] if descending else field
                if field_name not in {"name", "description", "group", "price"}:
                    continue
                column = getattr(self.table.c, field_name, None)
                if column is None:
                    continue
                order_clauses.append(column.desc() if descending else column.asc())
            if order_clauses:
                stmt = stmt.order_by(*order_clauses)

        rows = await self.session.execute(stmt)
        items = [self.entity.model_validate(dict(row)) for row in rows.mappings().all()]
        return PaginatedEntities(items=items, total=total)

    async def get_by_unique(self, *, name: str, group: str | None) -> Price | None:
        stmt = select(self.table).where(
            self.table.c.name == name,
            getattr(self.table.c, "group") == group,
        )
        row = await self.session.execute(stmt)
        mapping = row.mappings().first()
        if mapping is None:
            return None
        return self.entity.model_validate(dict(mapping))

    async def list_groups(self) -> list[str]:
        stmt = (
            select(self.table.c.group)
            .distinct()
            .where(self.table.c.group.is_not(None))
            .order_by(self.table.c.group.asc())
        )
        rows = await self.session.execute(stmt)
        return [row[0] for row in rows.all()]


class PriceVariantRepository(AbstractRepository[PriceVariant]):
    table: Table = price_variants
    entity = PriceVariant

    async def get_all_price_variants(
        self,
        *,
        price_ids: list[UUID] | None = None,
    ) -> list[PriceVariant]:
        stmt = select(self.table)
        if price_ids:
            stmt = stmt.where(self.table.c.price_id.in_(price_ids))

        rows = await self.session.execute(stmt)
        return [self.entity.model_validate(dict(row)) for row in rows.mappings().all()]

    async def get_by_unique(self, *, name: str, price_id: UUID) -> PriceVariant | None:
        stmt = select(self.table).where(
            self.table.c.name == name,
            self.table.c.price_id == price_id,
        )
        row = await self.session.execute(stmt)
        mapping = row.mappings().first()
        if mapping is None:
            return None
        return self.entity.model_validate(dict(mapping))
