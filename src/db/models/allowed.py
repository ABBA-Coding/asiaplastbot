"""AllowedSeller model file."""
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AllowedSeller(Base):
    """AllowedSeller model."""

    phone_number: Mapped[str] = mapped_column(sa.String(length=20), unique=False, nullable=True)