"""Feedback repository file."""

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base, Feedback
from .abstract import Repository


class FeedbackRepo(Repository[Feedback]):
    """Feedback repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize Feedback repository as for all Feedbacks or only for one Feedback."""
        super().__init__(type_model=Feedback, session=session)

    async def new(
        self,
        message: str,
        user_id: int,
    ) -> None:
        await self.session.merge(
            Feedback(
                message=message,
                user_id=user_id,
            )
        )            
