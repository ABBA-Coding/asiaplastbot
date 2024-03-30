"""Cashback model file."""
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship, lazyload

from typing import Annotated, Optional

from .base import Base

from ...bot.utils.formatters import price_formatter


class Cashback(Base):
    """Cashback model."""

    price: Mapped[int] = mapped_column(
        sa.Integer, unique=False, nullable=False
    )
    check_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False
    )
    status: Mapped[bool] = mapped_column(
        sa.Boolean, unique=False, nullable=False
    )
    client_id: Mapped[int] = mapped_column(
        sa.ForeignKey('client.user_id', ondelete='CASCADE'),
        unique=False,
        nullable=True,
    )
    client = relationship("Client", back_populates="cashbacks")
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    @property
    def formatted_price(self) -> int:
        return price_formatter(self.price)
    
    @property
    def cashback_sum(self) -> int:
        return price_formatter((self.price / 100) * 4)
    
    @property
    def client_phone_number(self) -> str:
        return f"{self.client.phone_number}"
    
    def __str__(self):
        return "Keshbeklar"
