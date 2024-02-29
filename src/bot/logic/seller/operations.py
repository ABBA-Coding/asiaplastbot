import random, qrcode

from sqlalchemy.exc import IntegrityError

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.cache import Cache
from src.db.database import Database
from src.language.translator import LocaleScheme, LocalizedTranslator
from .router import seller_router
from ...structures.fsm.category import CategoryGroup
from ...structures.keyboards import common


@seller_router.message(F.text=="Tovar sotish")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    await state.set_state(CategoryGroup.price)

    return await message.answer(
        translator.get("price")
    )


@seller_router.message(F.text.isdigit(), CategoryGroup.price)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    await state.update_data({
        'price': message.text
    })
    await state.set_state(CategoryGroup.confirm)

    formatted_number = '{:,}'.format(int(message.text)).replace(',', '.')
    return await message.answer(
        f"{formatted_number} {translator.get('confirm')}",
        reply_markup=common.confirm()
    )


@seller_router.message(F.text.in_({"Tasdiqlash", "Bekor qilish", "Menyuga qaytish"}), CategoryGroup.confirm)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    if message.text != "Tasdiqlash":
        await state.clear()


    else:
        random_number = random.randint(10000000, 99999999)
        img = qrcode.make(f"https://t.me/teeessstbot?start={random_number}")
        img.save(f"{random_number}.png")

@seller_router.message(F.text=="Mening keshbeklarim")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    return await message.answer("Test")


@seller_router.message(F.text=="Keshbeklar tarixi")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    return await message.answer("Test")


@seller_router.message(F.text=="Aloqa")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    return await message.answer("Test")


@seller_router.message(F.text=="Feedback")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    return await message.answer("Test")


@seller_router.message(F.text=="Sozlamalarim")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    return await message.answer("Test")
