"""Purchase repository file."""

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base, Purchase
from .abstract import Repository


class PurchaseRepo(Repository[Purchase]):
    """Purchase repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize Purchase repository as for all Purchases or only for one Purchase."""
        super().__init__(type_model=Purchase, session=session)

    async def new(
        self,
        product_id: int,
        client_id: int,
        region: str,
    ) -> None:
        await self.session.merge(
            Purchase(
                product_id=product_id,
                client_id=client_id,
                region=region,
            )
        )            
