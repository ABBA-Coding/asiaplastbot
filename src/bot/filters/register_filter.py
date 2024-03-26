from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.db.database import Database


class RegisterFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        async with AsyncSession(bind=kwargs['engine']) as session:
            db = Database(session)
            seller = await db.seller.get_me(message.from_user.id)
            client = await db.client.get_me(message.from_user.id)
            if seller or client:
                return False
            return True
        

class RegisterFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        async with AsyncSession(bind=kwargs['engine']) as session:
            db = Database(session)
            seller = await db.seller.get_me(message.from_user.id)
            client = await db.client.get_me(message.from_user.id)
            if seller or client:
                return False
            return True


class SellerFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        async with AsyncSession(bind=kwargs['engine']) as session:
            db = Database(session)
            seller = await db.seller.get_me(message.from_user.id)

            if seller:
                return True
            return False


class ClientFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        async with AsyncSession(bind=kwargs['engine']) as session:
            db = Database(session)
            client = await db.client.get_me(message.from_user.id)

            if client:
                return True
            return False
