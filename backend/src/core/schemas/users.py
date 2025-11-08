from pydantic import Field

from core.entities import User as UserEntity
from core.schemas.baseschema import BaseSchema


class UserOutDto(UserEntity, BaseSchema):
    password: str = Field(exclude=True)
