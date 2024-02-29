"""Product repository file."""

from sqlalchemy import select, and_, update
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
        check_id: int,
        qr_image_path: str,
        qr_image_file_id: str,
        status: bool,
        seller_id: int,
    ) -> None:
        await self.session.merge(
            Product(
                price=price,
                check_id=check_id,
                qr_image_path=qr_image_path,
                qr_image_file_id=qr_image_file_id,
                status=status,
                seller_id=seller_id,
            )
        )

    async def get_sold_products(self, seller_id: int):
        condition1 = Product.seller_id == seller_id
        condition2 = Product.status == True
        whereclause = and_(condition1, condition2)

        all_data = await super().get_many(
            whereclause=whereclause
        )
        return all_data    

    async def get_product_by_check_id(self, check_id: int):
        """Get Product by user_id."""
        return await self.session.scalar(
            select(Product).where(Product.check_id == check_id).limit(1)
        )

    async def edit(self, check_id: int, **data):
        stmt = update(Product).where(Product.check_id == check_id).values(**data)
        await self.session.execute(stmt)