"""Client model file."""
import datetime
from typing import Annotated, Optional
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.cashback import Cashback
from src.db.models.product import Product

from .base import Base


class Client(Base):
    """Client model."""

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False
    )
    fullname: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=False
    )
    phone_number: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    language: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    product_id: Mapped[int] = mapped_column(
        sa.ForeignKey('product.id'),
        unique=False,
        nullable=True,
    )
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

