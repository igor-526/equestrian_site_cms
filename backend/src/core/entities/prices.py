from enum import StrEnum, auto
from uuid import UUID

from pydantic import Field

from .base import Entity, TimeStampMixin


class PriceFormatter(StrEnum):
    """Форматы цены услуги."""

    equal = auto()
    lt = auto()
    gt = auto()
    discuss = auto()


class Price(Entity):
    """Цены услуг."""

    name: str = Field(
        default=...,
        description="Наименование услуги",
        examples=["Катание на лошади"],
    )
    description: str | None = Field(
        default=None,
        description="Описание услуги",
        examples=["В будний день"],
    )
    group: str | None = Field(
        default=None,
        description="Группа услуги",
        examples=["Катания"],
    )
    price: int = Field(
        default=0,
        description="Основная цена услуги",
        examples=[1000],
    )
    price_formatter: PriceFormatter = Field(
        default=PriceFormatter.equal,
        description="Формат основной цены услуги",
        examples=["equal", "gt", "lt", "discuss"],
    )


class PriceVariant(Entity):
    price_id: UUID = Field(
        default=...,
        description="Идентификатор цены",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    name: str = Field(
        default=...,
        description="Наименование варианта цены",
        examples=["Катание на лошади в будний день"],
    )
    description: str | None = Field(
        default=None,
        description="Описание варианта цены",
        examples=["Катание на лошади в будний день"],
    )
    price: int = Field(
        default=0,
        description="Цена варианта цены",
        examples=[1000],
    )
    price_formatter: PriceFormatter = Field(
        default=PriceFormatter.equal,
        description="Формат варианта цены",
        examples=["equal", "gt", "lt", "discuss"],
    )
