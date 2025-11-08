from uuid import UUID

from pydantic import Field

from core.entities import Price, PriceFormatter, PriceVariant
from core.schemas.baseschema import BaseSchema


class PriceVariantCreateInDto(BaseSchema):
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


class PriceVariantUpdateInDto(BaseSchema):
    name: str | None = Field(
        default=None,
        description="Наименование варианта цены",
        examples=["Катание на лошади в будний день"],
    )
    description: str | None = Field(
        default=None,
        description="Описание варианта цены",
        examples=["Катание на лошади в будний день"],
    )
    price: int | None = Field(
        default=None,
        description="Цена варианта цены",
        examples=[1000],
    )
    price_formatter: PriceFormatter | None = Field(
        default=None,
        description="Формат варианта цены",
        examples=["equal", "gt", "lt", "discuss"],
    )


class PriceVariantOutDto(PriceVariant, BaseSchema):
    price_id: UUID = Field(exclude=True)


class PriceCreateInDto(BaseSchema):
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
    variants: list[PriceVariantCreateInDto] | None = Field(
        default_factory=list,
        description="Варианты цены",
    )


class PriceUpdateInDto(BaseSchema):
    name: str | None = Field(
        default=None,
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
    price: int | None = Field(
        default=None,
        description="Основная цена услуги",
        examples=[1000],
    )
    price_formatter: PriceFormatter | None = Field(
        default=None,
        description="Формат основной цены услуги",
        examples=["equal", "gt", "lt", "discuss"],
    )


class PriceOutDto(Price, BaseSchema):
    variants: list[PriceVariantOutDto] | None = Field(
        default_factory=list,
        description="Варианты цены",
    )
