"""Allowed repository file."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base, AllowedSeller
from .abstract import Repository


class AllowedRepo(Repository[AllowedSeller]):
    """Allowed repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize Allowed repository as for all Alloweds or only for one Allowed."""
        super().__init__(type_model=AllowedSeller, session=session)

    async def new(
        self,
        phone_number: str,
    ) -> None:
        await self.session.merge(
            AllowedSeller(
                phone_number=phone_number,
            )
        )

    async def get_allowed_sellers(self):
        all_data = await super().get_many()
        
        res = [obj.phone_number for obj in all_data if obj]
        return res
