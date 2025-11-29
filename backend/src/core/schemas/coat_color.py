from datetime import datetime
from uuid import UUID

from pydantic import Field, field_serializer

from core.entities.coat_color import CoatColor
from core.schemas.baseschema import BaseSchema


class CoatColorOutDto(BaseSchema):
    """DTO для вывода масти."""

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


class CoatColorOutWithPageDataDto(CoatColorOutDto):
    """DTO для вывода масти с page_data."""

    page_data: str


class CoatColorCreateDto(BaseSchema):
    """DTO для создания масти."""

    name: str = Field(..., description="Название масти")
    slug: str | None = Field(None, description="Slug (опционально, генерируется автоматически)")
    description: str | None = Field(None, description="Описание масти")
    page_data: str | None = Field(None, description="Данные страницы в формате HTML/текста")


class CoatColorUpdateDto(BaseSchema):
    """DTO для обновления масти."""

    name: str | None = Field(None, description="Название масти")
    slug: str | None = Field(None, description="Slug")
    description: str | None = Field(None, description="Описание масти")
    page_data: str | None = Field(None, description="Данные страницы в формате HTML/текста")

