"""Data Structures.

This file contains TypedDict structure to store data which will
transfer throw Dispatcher->Middlewares->Handlers.
"""

from typing import TypedDict

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncEngine

from src.bot.structures.role import Role
from src.db.database import Database

from src.language.translator import Translator, LocalizedTranslator
from src.language.enums import Locales

class TransferData(TypedDict):
    """Common transfer data."""

    translator: Translator | LocalizedTranslator
    engine: AsyncEngine
    db: Database
    bot: Bot
    role: Role


class TransferUserData(TypedDict):
    role: Role
    locale: Locales
