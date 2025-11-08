import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from core.entities import PaginatedEntities
from core.schemas.prices import (
    PriceCreateInDto,
    PriceOutDto,
    PriceUpdateInDto,
    PriceVariantCreateInDto,
    PriceVariantOutDto,
    PriceVariantUpdateInDto,
)
from core.schemas.users import UserOutDto
from core.services.prices import PriceService
from depends.services import get_current_user, get_price_service

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedEntities[PriceOutDto],
    summary="Получение всех цен",
)
async def list_prices(
    price_service: Annotated[PriceService, Depends(get_price_service)],
    limit: int | None = Query(default=25, ge=0, description="Количество элементов"),
    offset: int | None = Query(default=0, ge=0, description="Смещение"),
    name: str | None = Query(default=None, description="Фильтр по названию"),
    description: str | None = Query(default=None, description="Фильтр по описанию"),
    group: list[str] | None = Query(
        default=None,
        description="Список групп услуг для фильтрации",
        alias="group[]",
    ),
    price_gt: int | None = Query(
        default=None,
        ge=0,
        description="Фильтр по цене: строго больше указанного значения",
    ),
    price_lt: int | None = Query(
        default=None,
        ge=0,
        description="Фильтр по цене: строго меньше указанного значения",
    ),
    sort: list[str] | None = Query(
        default=None,
        description="Список полей сортировки (напр. name, -price)",
        alias="sort[]",
    ),
) -> PaginatedEntities[PriceOutDto]:
    return await price_service.list_prices(
        limit=limit,
        offset=offset,
        name=name,
        description=description,
        group=group,
        price_gt=price_gt,
        price_lt=price_lt,
        sort=sort,
    )


@router.post(
    "",
    response_model=PriceOutDto,
    status_code=status.HTTP_201_CREATED,
    summary="Создание новой цены",
)
async def create_price(
    price_service: Annotated[PriceService, Depends(get_price_service)],
    _: Annotated[UserOutDto, Depends(get_current_user)],
    data: PriceCreateInDto,
) -> PriceOutDto:
    return await price_service.create_price(data=data)


@router.put(
    "/{price_id}",
    response_model=PriceOutDto,
    summary="Обновление цены",
)
async def update_price(
    price_service: Annotated[PriceService, Depends(get_price_service)],
    _: Annotated[UserOutDto, Depends(get_current_user)],
    price_id: uuid.UUID,
    data: PriceUpdateInDto,
) -> PriceOutDto:
    return await price_service.update_price(price_id=price_id, data=data)


@router.delete(
    "/{price_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление цены",
)
async def delete_price(
    price_service: Annotated[PriceService, Depends(get_price_service)],
    _: Annotated[UserOutDto, Depends(get_current_user)],
    price_id: uuid.UUID,
) -> None:
    await price_service.delete_price(price_id=price_id)


@router.post(
    "/{price_id}/variants",
    response_model=PriceVariantOutDto,
    status_code=status.HTTP_201_CREATED,
    summary="Создание варианта цены",
)
async def add_price_variant(
    price_service: Annotated[PriceService, Depends(get_price_service)],
    _: Annotated[UserOutDto, Depends(get_current_user)],
    price_id: uuid.UUID,
    data: PriceVariantCreateInDto,
) -> PriceVariantOutDto:
    return await price_service.add_price_variant(price_id=price_id, data=data)


@router.put(
    "/{price_id}/variants/{variant_id}",
    response_model=PriceVariantOutDto,
    summary="Обновление варианта цены",
)
async def update_price_variant(
    price_service: Annotated[PriceService, Depends(get_price_service)],
    _: Annotated[UserOutDto, Depends(get_current_user)],
    price_id: uuid.UUID,
    variant_id: uuid.UUID,
    data: PriceVariantUpdateInDto,
) -> PriceVariantOutDto:
    return await price_service.update_price_variant(
        price_id=price_id,
        price_variant_id=variant_id,
        data=data,
    )


@router.delete(
    "/{price_id}/variants/{variant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление варианта цены",
)
async def delete_price_variant(
    price_service: Annotated[PriceService, Depends(get_price_service)],
    _: Annotated[UserOutDto, Depends(get_current_user)],
    price_id: uuid.UUID,
    variant_id: uuid.UUID,
) -> None:
    await price_service.delete_price_variant(
        price_id=price_id,
        price_variant_id=variant_id,
    )


@router.get(
    "/groups",
    response_model=list[str],
    summary="Получение всех групп цен",
)
async def list_price_groups(
    price_service: Annotated[PriceService, Depends(get_price_service)],
) -> list[str]:
    return await price_service.list_price_groups()
