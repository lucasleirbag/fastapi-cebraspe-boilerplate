from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import User
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    async def get_by_username(
        self, username: str, join_: set[str] | None = None
    ) -> User | None:
        query = self._query(join_)
        query = query.filter(User.username == username)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._one_or_none(query)

    async def get_by_email(
        self, email: str, join_: set[str] | None = None
    ) -> User | None:
        query = self._query(join_)
        query = query.filter(User.email == email)

        if join_ is not None:
            return await self.all_unique(query)
   
        return await self._one_or_none(query)

    def _join_tasks(self, query: Select) -> Select:
        return query.options(joinedload(User.tasks)).execution_options(
            contains_joined_collection=True
        )
