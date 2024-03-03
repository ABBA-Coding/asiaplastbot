from sqlalchemy.exc import IntegrityError

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.cache import Cache
from src.db.database import Database
from src.bot.filters.admin_filter import AdminFilter
from src.language.translator import LocaleScheme, LocalizedTranslator
from .router import admin_router
from ...structures.fsm.registration import RegisterGroup
from ...structures.keyboards import common
from ...utils.formatters import price_formatter


@admin_router.message(F.text=='/admin', AdminFilter())
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    cache: Cache
):
    await message.answer(
        "Admin panelga Hush kelibsiz!",
        reply_markup=common.admin_dashboard()
    )


@admin_router.message(F.text == "Sotuvchini qo'shish")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    cache: Cache
):
    await message.answer(
        "Iltimos telefon raqamini jo'nating",
        reply_markup=types.ReplyKeyboardRemove()
    )


@admin_router.message(F.contact)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    cache: Cache,
    db: Database
):
    await db.allowed.new(
        phone_number=message.contact.phone_number
    )
    await db.session.commit()

    await message.answer(
        "Sotuvchilar ro'yhatiga qo'shildi!",
        reply_markup=common.admin_dashboard()
    )