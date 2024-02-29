"""Product repository file."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base, Product
from .abstract import Repository


class ProductRepo(Repository[Product]):
    """Product repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize Product repository as for all Products or only for one Product."""
        super().__init__(type_model=Product, session=session)

    async def new(
        self,
        price: int,
        check_id: int | None = None,
        status: bool | None = None,
    ) -> None:
        await self.session.merge(
            Product(
                price=price,
                check_id=check_id,
                status=status,
            )
        )