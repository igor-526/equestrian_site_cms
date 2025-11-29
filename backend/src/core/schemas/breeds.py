from datetime import datetime
from uuid import UUID

from pydantic import Field, field_serializer

from core.entities.breeds import Breed
from core.schemas.baseschema import BaseSchema


class BreedOutDto(BaseSchema):
    """DTO для вывода породы."""

    id: UUID
    name: str
    slug: str
    description: str | None
    created_at: datetime
    updated_at: datetime | None

    @field_serializer("id")
    def serialize_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        return value.isoformat()

    class Config:
        from_attributes = True


class BreedOutWithPageDataDto(BreedOutDto):
    """DTO для вывода породы с page_data."""

    page_data: str


class BreedCreateDto(BaseSchema):
    """DTO для создания породы."""

    name: str = Field(..., description="Название породы")
    slug: str | None = Field(None, description="Slug (опционально, генерируется автоматически)")
    description: str | None = Field(None, description="Описание породы")
    page_data: str | None = Field(None, description="Данные страницы в формате HTML/текста")


class BreedUpdateDto(BaseSchema):
    """DTO для обновления породы."""

    name: str | None = Field(None, description="Название породы")
    slug: str | None = Field(None, description="Slug")
    description: str | None = Field(None, description="Описание породы")
    page_data: str | None = Field(None, description="Данные страницы в формате HTML/текста")

