"""Client repository file."""

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
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
        product_id: int | None = None,
    ) -> None:
        await self.session.merge(
            Client(
                user_id=user_id,
                fullname=fullname,
                phone_number=phone_number,
                language=language,
                product_id=product_id,
            )
        )

    async def add_or_update(self, **kwargs):
        insert_stmt = insert(Client).values(**kwargs)
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=(Client.user_id,), set_=kwargs, where=Client.user_id == kwargs['user_id']
        ).returning(Client)

        await self.session.execute(do_update_stmt)
            
