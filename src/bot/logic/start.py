"""This file represents a start logic."""

from sqlalchemy.exc import IntegrityError
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from src.bot.filters.register_filter import RegisterFilter
from src.db.database import Database
from src.language.translator import LocalizedTranslator
from ..structures.fsm.registration import RegisterGroup
from ..structures.keyboards import common

start_router = Router(name='start')


@start_router.message(CommandStart(), RegisterFilter())
async def start_handler(message: types.Message, db: Database, translator: LocalizedTranslator, state: FSMContext):
    """Start command handler."""
    await state.clear()

    try:
        await db.user.new(
            user_id=message.from_user.id,
            user_name=message.from_user.username,
            first_name=message.from_user.first_name,
            second_name=message.from_user.last_name,
            is_premium=bool(message.from_user.is_premium),
        )
        await db.session.commit()
    except IntegrityError:
        await db.session.rollback()
        print("User already exists")

    texts = message.text.split()
    print(message.text)

    if len(texts) == 2 and texts[1].isdigit():
        product = await db.product.get_product_by_check_id(int(texts[1]))

        if product:
            await state.update_data({
                'deep_link': int(texts[1]),
                'product_id': product.id,
                # 'region': product.seller.region,
                'price': product.price,
                'seller_id': product.seller_id,
            })
        
    await state.set_state(RegisterGroup.lang)
    await message.answer(
        "Tilni tanlang\n"
        "Выберите язык\n",
        reply_markup=common.show_languages()
    )


@start_router.message(CommandStart())
async def restart_handler(
    message: types.Message, 
    translator: LocalizedTranslator,
    state: FSMContext
):
    """Start command handler."""
    await message.answer(
        translator.get("menu"),
        reply_markup=common.category()
    )
    await state.clear()
