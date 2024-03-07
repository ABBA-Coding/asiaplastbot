"""Client model file."""
import datetime
from typing import Annotated, Optional
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column


from .base import Base


class Purchase(Base):
    """Client model."""
    client_id: Mapped[int] = mapped_column(
        sa.ForeignKey('client.user_id', ondelete='CASCADE'),
        unique=False,
        nullable=True,
        type_=BIGINT
    )
    product_id: Mapped[int] = mapped_column(
        sa.ForeignKey('product.id', ondelete='CASCADE'),
        unique=False,
        nullable=True,
    )
    client = orm.relationship("Client", back_populates="purchases", lazy="joined")
    product = orm.relationship("Product", back_populates="purchases", lazy="joined")

    region: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    
    created_at: Mapped[Optional[Annotated[datetime.datetime, mapped_column(nullable=False, default=datetime.datetime.utcnow)]]]

    def __str__(self):
        return "Haridlar"
