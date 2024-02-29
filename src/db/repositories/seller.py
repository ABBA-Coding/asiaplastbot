"""Seller repository file."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role

from ..models import Base, Seller
from .abstract import Repository


class SellerRepo(Repository[Seller]):
    """Seller repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize Seller repository as for all Sellers or only for one Seller."""
        super().__init__(type_model=Seller, session=session)

    async def new(
        self,
        user_id: int,
        fullname: str | None = None,
        phone_number: str | None = None,
        region: str | None = None,
        language: str | None = None,
    ) -> None:
        await self.session.merge(
            Seller(
                user_id=user_id,
                fullname=fullname,
                phone_number=phone_number,
                region=region,
                language=language,
            )
        )

    # async def get_role(self, seller_id: int) -> Role:
    #     """Get Seller role by id."""
    #     return await self.session.scalar(
    #         select(Seller.role).where(Seller.Seller_id == Seller_id).limit(1)
    #     )
