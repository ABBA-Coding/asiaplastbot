"""Cashback repository file."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base, Cashback
from .abstract import Repository


class CashbackRepo(Repository[Cashback]):
    """Cashback repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize Cashback repository as for all Cashbacks or only for one Cashback."""
        super().__init__(type_model=Cashback, session=session)

    async def new(
        self,
        price: int,
        check_id: int | None = None,
        status: bool | None = None,
    ) -> None:
        await self.session.merge(
            Cashback(
                price=price,
                check_id=check_id,
                status=status,
            )
        )