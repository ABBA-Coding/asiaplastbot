"""AllowedSeller model file."""
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AllowedSeller(Base):
    """AllowedSeller model."""

    phone_number: Mapped[str] = mapped_column(sa.Text, unique=False, nullable=True)