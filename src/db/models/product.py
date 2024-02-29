"""Product model file."""
import datetime
import sqlalchemy as sa

from typing import Annotated, Optional
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


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
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

