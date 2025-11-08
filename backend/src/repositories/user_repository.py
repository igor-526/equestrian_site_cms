from sqlalchemy import Table, select

from core.entities.user import User
from models.users import users

from .abstract_repository import AbstractRepository


class UserRepository(AbstractRepository[User]):
    table: Table = users
    entity = User

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(self.table).where(self.table.c.username == username)
        row = await self.session.execute(stmt)
        mapping = row.mappings().first()
        if mapping is None:
            return None
        return self.entity.model_validate(dict(mapping))
