"""Product model file."""
import datetime
import sqlalchemy as sa

from typing import Annotated, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from src.db.models.purchase import Purchase


class Feedback(Base):
    """Product model."""

    message: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey('user.user_id', ondelete='CASCADE'),
        unique=False,
        nullable=True,
    )
    user = relationship("User", back_populates="feedbacks", lazy="joined")
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    def __str__(self):
        return "Fikrlar"
