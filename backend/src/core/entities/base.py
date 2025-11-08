from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TimeStampMixin(BaseModel):
    """Миксин с временными метками создания и обновления."""

    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Момент создания сущности",
    )
    updated_at: datetime | None = Field(
        default_factory=datetime.now,
        description="Момент последнего обновления",
    )


class Entity(BaseModel):
    """Базовая сущность с уникальным идентификатором."""

    id: UUID = Field(
        default_factory=uuid4,
        description="Уникальный идентификатор сущности",
    )
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def _check_invariants(self) -> "Entity":
        return self


class PaginatedEntities[T: Entity](BaseModel):
    items: list[T] = Field(
        default_factory=list,
        description="Список элементов",
    )
    total: int = Field(
        default=0,
        description="Общее количество элементов",
    )
