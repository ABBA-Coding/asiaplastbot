"""Cashback repository file."""
from datetime import datetime, timedelta

from sqlalchemy import select, and_
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
        check_id: int,
        status: bool,
        seller_id: int,
    ) -> None:
        await self.session.merge(
            Cashback(
                price=price,
                check_id=check_id,
                status=status,
                seller_id=seller_id
            )
        )

    async def get_cashbacks_by_seller_id(self, seller_id: int):
        all_data = await super().get_many(
            whereclause=Cashback.seller_id == seller_id
        )
        res = [obj.price for obj in all_data if obj]
        return res

    async def get_last_cashbacks(self, seller_id: int, delta: datetime = None):
        if delta:
            condition1 = Cashback.seller_id == seller_id
            condition2 = Cashback.created_at >= delta
            whereclause = and_(condition1, condition2)
        
        else:
            whereclause = Cashback.seller_id == seller_id

        all_data = await super().get_many(
            whereclause=whereclause
        )
        return all_data