"""Client model file."""
import datetime
from typing import Annotated, Optional
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.purchase import Purchase

from .base import Base


class Client(Base):
    """Client model."""

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False, index=True, primary_key=True
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
    purchases: Mapped[Purchase] = orm.relationship(
        'Purchase', uselist=False, lazy='joined', back_populates="client"
    )
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    def __str__(self):
        return self.fullname
