"""Cashback model file."""
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import Annotated, Optional

from .base import Base


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
    seller_id: Mapped[int] = mapped_column(
        sa.ForeignKey('seller.user_id', ondelete='CASCADE'),
        unique=False,
        nullable=True,
    )
    seller = relationship("Seller", back_populates="cashbacks", lazy="joined")
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]


    def __str__(self):
        return "Keshbeklar"
