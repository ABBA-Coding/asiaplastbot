"""Client repository file."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base, Client
from .abstract import Repository


class ClientRepo(Repository[Client]):
    """Client repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize Client repository as for all Clients or only for one Client."""
        super().__init__(type_model=Client, session=session)

    async def new(
        self,
        user_id: int,
        fullname: str | None = None,
        phone_number: str | None = None,
        language: str | None = None,
    ) -> None:
        await self.session.merge(
            Client(
                user_id=user_id,
                fullname=fullname,
                phone_number=phone_number,
                language=language,
            )
        )