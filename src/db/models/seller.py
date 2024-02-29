"""Seller model file."""
import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm

from typing import Annotated, Optional
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.cashback import Cashback
from src.db.models.product import Product

from .base import Base


class Seller(Base):
    """Seller model."""

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False, primary_key=True
    )
    fullname: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=False
    )
    phone_number: Mapped[str] = mapped_column(sa.Text, unique=False, nullable=True)
    region: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    language: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    products: Mapped[Product] = orm.relationship(
        'Product', uselist=False, lazy='joined'
    )
    cashbacks: Mapped[Cashback] = orm.relationship(
        'Cashback', uselist=False, lazy='joined'
    )
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]
