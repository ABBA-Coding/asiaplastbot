"""Product model file."""
import datetime
import sqlalchemy as sa

from typing import Annotated, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from src.db.models.purchase import Purchase

from ...bot.utils.formatters import price_formatter


class Product(Base):
    """Product model."""

    price: Mapped[int] = mapped_column(
        sa.Integer, unique=False, nullable=False
    )
    check_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False
    )
    qr_image_path: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=False
    )
    qr_image_file_id: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=False
    )
    status: Mapped[bool] = mapped_column(
        sa.Boolean, unique=False, nullable=False
    )
    seller_id: Mapped[int] = mapped_column(
        sa.ForeignKey('seller.user_id', ondelete='CASCADE'),
        unique=False,
        nullable=True,
    )
    purchases: Mapped[Purchase] = relationship(
        'Purchase', uselist=False, lazy='joined', back_populates="product"
    )
    seller = relationship("Seller", back_populates="products")
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    @property
    def formatted_price(self) -> int:
        return price_formatter(self.price)
    
    @property
    def seller_phone_number(self) -> str:
        return f"{self.seller.phone_number}"
    
    def __str__(self):
        return "Tovar"
