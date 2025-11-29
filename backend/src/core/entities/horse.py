from datetime import date
from uuid import UUID

from pydantic import Field

from .base import Entity, SlugMixin, TimeStampMixin


class Horse(Entity, TimeStampMixin, SlugMixin):
    """Лошадь."""

    name: str = Field(
        default=...,
        description="Имя лошади",
        examples=["Арабский жеребец"],
    )
    description: str | None = Field(
        default=None,
        description="Описание лошади",
        examples=["Красивый и быстрый жеребец"],
    )
    breed_id: UUID | None = Field(
        default=None,
        description="Идентификатор породы",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    coat_color_id: UUID | None = Field(
        default=None,
        description="Идентификатор масти",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    kind: str = Field(
        default=...,
        description="Вид лошади",
        examples=["horse"],
    )
    height: int | None = Field(
        default=None,
        description="Рост в сантиметрах",
        examples=[165],
    )
    sex: str = Field(
        default=...,
        description="Пол лошади",
        examples=["male"],
    )
    bdate: date | None = Field(
        default=None,
        description="Дата рождения",
        examples=["2020-01-01"],
    )
    ddate: date | None = Field(
        default=None,
        description="Дата смерти",
        examples=["2023-01-01"],
    )
    bdate_mode: str = Field(
        default="0",
        description="Режим отображения даты рождения",
        examples=["0"],
    )
    ddate_mode: str = Field(
        default="0",
        description="Режим отображения даты смерти",
        examples=["0"],
    )
    horse_owner_id: UUID | None = Field(
        default=None,
        description="Идентификатор владельца",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )


class HorseChildren(Entity, TimeStampMixin):
    """Связь родитель-потомок между лошадьми."""

    horse_id: UUID = Field(
        default=...,
        description="Идентификатор родительской лошади",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    child_id: UUID = Field(
        default=...,
        description="Идентификатор дочерней лошади",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )


class HorsePhotos(Entity, TimeStampMixin):
    """Связь между лошадью и фотографией."""

    horse_id: UUID = Field(
        default=...,
        description="Идентификатор лошади",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    photo_id: UUID = Field(
        default=...,
        description="Идентификатор фотографии",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    is_main: bool = Field(
        default=False,
        description="Является ли фотография главной",
        examples=[True],
    )
