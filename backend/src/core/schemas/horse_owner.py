from datetime import datetime
from uuid import UUID

from pydantic import Field, field_serializer, field_validator

from core.entities.horse_owner import HorseOwner, HorseOwnerType
from core.schemas.baseschema import BaseSchema


class HorseOwnerOutDto(BaseSchema):
    """DTO для вывода владельца."""

    id: UUID
    name: str
    description: str | None
    type: HorseOwnerType
    address: str | None
    phone_numbers: list[str]
    created_at: datetime
    updated_at: datetime | None

    @field_serializer("id")
    def serialize_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer("type")
    def serialize_type(self, value: HorseOwnerType) -> str:
        return str(value)

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        return value.isoformat()

    class Config:
        from_attributes = True


class HorseOwnerCreateDto(BaseSchema):
    """DTO для создания владельца."""

    name: str = Field(..., description="Имя владельца")
    description: str | None = Field(None, description="Описание владельца")
    type: HorseOwnerType = Field(HorseOwnerType.person, description="Тип владельца")
    address: str | None = Field(None, description="Адрес владельца")
    phone_numbers: list[str] = Field(default_factory=list, description="Список телефонных номеров")

    @field_validator("phone_numbers")
    @classmethod
    def validate_phone_numbers(cls, v: list[str]) -> list[str]:
        """Валидация формата телефонов: должен начинаться с + и содержать от 7 до 15 цифр."""
        from core.exceptions.base import ClientError
        import re
        # Международный формат: + и от 7 до 15 цифр
        pattern = r"^\+\d{7,15}$"
        for phone in v:
            if not re.match(pattern, phone):
                raise ClientError(
                    f"Неверный формат телефона: {phone}. "
                    "Телефон должен начинаться с + и содержать от 7 до 15 цифр"
                )
        return v


class HorseOwnerUpdateDto(BaseSchema):
    """DTO для обновления владельца."""

    name: str | None = Field(None, description="Имя владельца")
    description: str | None = Field(None, description="Описание владельца")
    type: HorseOwnerType | None = Field(None, description="Тип владельца")
    address: str | None = Field(None, description="Адрес владельца")
    phone_numbers: list[str] | None = Field(None, description="Список телефонных номеров")

    @field_validator("phone_numbers")
    @classmethod
    def validate_phone_numbers(cls, v: list[str] | None) -> list[str] | None:
        """Валидация формата телефонов: должен начинаться с + и содержать от 7 до 15 цифр."""
        if v is None:
            return v
        from core.exceptions.base import ClientError
        import re
        # Международный формат: + и от 7 до 15 цифр
        pattern = r"^\+\d{7,15}$"
        for phone in v:
            if not re.match(pattern, phone):
                raise ClientError(
                    f"Неверный формат телефона: {phone}. "
                    "Телефон должен начинаться с + и содержать от 7 до 15 цифр"
                )
        return v

