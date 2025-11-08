from collections import defaultdict
from uuid import UUID

from core.entities import PaginatedEntities, Price, PriceVariant
from core.exceptions.base import ClientError
from core.protocols.repositories import (
    PriceRepositoryProtocol,
    PriceVariantRepositoryProtocol,
)
from core.schemas.prices import (
    PriceCreateInDto,
    PriceOutDto,
    PriceUpdateInDto,
    PriceVariantCreateInDto,
    PriceVariantOutDto,
    PriceVariantUpdateInDto,
)


class PriceService:
    def __init__(
        self,
        price_repository: PriceRepositoryProtocol,
        price_variant_repository: PriceVariantRepositoryProtocol,
    ) -> None:
        self.price_repository = price_repository
        self.price_variant_repository = price_variant_repository

    async def list_prices(
        self,
        *,
        limit: int | None,
        offset: int | None,
        name: str | None,
        description: str | None,
        group: list[str] | None,
        price_gt: int | None,
        price_lt: int | None,
        sort: list[str] | None,
    ) -> PaginatedEntities[PriceOutDto]:
        prices = await self.price_repository.get_all_prices(
            limit=limit,
            offset=offset,
            name=name,
            description=description,
            group=group,
            price_gt=price_gt,
            price_lt=price_lt,
            sort=sort,
        )
        price_ids = [price.id for price in prices.items]
        variants = await self.price_variant_repository.get_all_price_variants(
            price_ids=price_ids if price_ids else None
        )

        variants_map: dict[UUID, list[PriceVariantOutDto]] = defaultdict(list)
        for variant in variants:
            variants_map[variant.price_id].append(
                PriceVariantOutDto.model_validate(variant)
            )

        result: list[PriceOutDto] = []
        for price in prices.items:
            price_out = PriceOutDto.model_validate(price)
            price_out.variants = variants_map.get(price.id, [])
            result.append(price_out)
        return PaginatedEntities(items=result, total=prices.total)

    async def create_price(self, *, data: PriceCreateInDto) -> PriceOutDto:
        if await self.price_repository.get_by_unique(
            name=data.name, group=data.group
        ):
            raise ClientError("Цена с таким названием и группой уже существует")

        price_payload = data.model_dump(exclude={"variants"})
        price_entity = Price(**price_payload)
        created_price = await self.price_repository.create(price_entity)

        created_variants: list[PriceVariantOutDto] = []
        for variant in data.variants or []:
            if await self.price_variant_repository.get_by_unique(
                name=variant.name, price_id=created_price.id
            ):
                raise ClientError(
                    f"Вариант цены с названием '{variant.name}' уже существует"
                )
            variant_entity = PriceVariant(
                price_id=created_price.id,
                **variant.model_dump(),
            )
            created_variant = await self.price_variant_repository.create(variant_entity)
            created_variants.append(PriceVariantOutDto.model_validate(created_variant))

        price_out = PriceOutDto.model_validate(created_price)
        price_out.variants = created_variants
        return price_out

    async def update_price(
        self,
        *,
        price_id: UUID,
        data: PriceUpdateInDto,
    ) -> PriceOutDto:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ClientError("Нет данных для обновления цены")

        price = await self.price_repository.get_by_id(price_id)
        if price is None:
            raise ClientError("Цена не найдена")

        name = update_data.get("name", price.name)
        group_value = update_data.get("group", price.group)
        if name != price.name or group_value != price.group:
            existing = await self.price_repository.get_by_unique(
                name=name, group=group_value
            )
            if existing and existing.id != price_id:
                raise ClientError("Цена с таким названием и группой уже существует")

        updated_price = price.model_copy(update=update_data)
        saved_price = await self.price_repository.update(updated_price)

        variants = await self.price_variant_repository.get_all_price_variants(
            price_ids=[price_id]
        )

        price_out = PriceOutDto.model_validate(saved_price)
        price_out.variants = [
            PriceVariantOutDto.model_validate(variant) for variant in variants
        ]
        return price_out

    async def delete_price(self, *, price_id: UUID) -> None:
        price = await self.price_repository.get_by_id(price_id)
        if price is None:
            raise ClientError("Цена не найдена")
        await self.price_repository.delete(price_id)

    async def add_price_variant(
        self,
        *,
        price_id: UUID,
        data: PriceVariantCreateInDto,
    ) -> PriceVariantOutDto:
        price = await self.price_repository.get_by_id(price_id)
        if price is None:
            raise ClientError("Цена не найдена")

        if await self.price_variant_repository.get_by_unique(
            name=data.name, price_id=price_id
        ):
            raise ClientError(
                f"Вариант цены с названием '{data.name}' уже существует"
            )

        variant_entity = PriceVariant(
            price_id=price_id,
            **data.model_dump(),
        )
        created_variant = await self.price_variant_repository.create(variant_entity)
        return PriceVariantOutDto.model_validate(created_variant)

    async def update_price_variant(
        self,
        *,
        price_id: UUID,
        price_variant_id: UUID,
        data: PriceVariantUpdateInDto,
    ) -> PriceVariantOutDto:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ClientError("Нет данных для обновления варианта цены")

        price = await self.price_repository.get_by_id(price_id)
        if price is None:
            raise ClientError("Цена не найдена")

        variant = await self.price_variant_repository.get_by_id(price_variant_id)
        if variant is None or variant.price_id != price_id:
            raise ClientError("Вариант цены не найден")

        new_name = update_data.get("name", variant.name)
        if new_name != variant.name:
            existing = await self.price_variant_repository.get_by_unique(
                name=new_name, price_id=price_id
            )
            if existing and existing.id != price_variant_id:
                raise ClientError(
                    f"Вариант цены с названием '{new_name}' уже существует"
                )

        updated_variant = variant.model_copy(update=update_data)
        saved_variant = await self.price_variant_repository.update(updated_variant)
        return PriceVariantOutDto.model_validate(saved_variant)

    async def delete_price_variant(
        self,
        *,
        price_id: UUID,
        price_variant_id: UUID,
    ) -> None:
        price = await self.price_repository.get_by_id(price_id)
        if price is None:
            raise ClientError("Цена не найдена")

        variant = await self.price_variant_repository.get_by_id(price_variant_id)
        if variant is None or variant.price_id != price_id:
            raise ClientError("Вариант цены не найден")

        await self.price_variant_repository.delete(price_variant_id)

    async def list_price_groups(self) -> list[str]:
        return await self.price_repository.list_groups()