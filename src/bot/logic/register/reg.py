from sqlalchemy.exc import IntegrityError

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.cache import Cache
from src.db.database import Database
from src.language.translator import LocaleScheme, LocalizedTranslator
from .router import register_router
from ...structures.fsm.registration import RegisterGroup
from ...structures.keyboards import common


@register_router.message(F.text.in_({"🇺🇿 O'zbek", "🇷🇺 Русский"}), RegisterGroup.lang)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    cache: Cache
):
    await state.set_state(RegisterGroup.fullname)
    d = {
        "🇺🇿 O'zbek": ["uz", "Iltimos ismingizni kiriting"],
        "🇷🇺 Русский": ["ru", "Введите свое имя"],
    }
    await state.update_data({
        'language': d.get(message.text)[0].upper()
    })
    user = message.from_user
    lang = d.get(message.text)[0]
    locale_key = LocaleScheme(user_id=user.id)
    await cache.set(locale_key, lang)

    return await message.answer(
        d.get(message.text)[1], reply_markup=types.ReplyKeyboardRemove()
    )


@register_router.message(F.text, RegisterGroup.fullname)
async def process_registration(message: Message, state: FSMContext, translator: LocalizedTranslator):
    await state.update_data({
        'fullname': message.text
    })
    await state.set_state(RegisterGroup.phone_number)
    return await message.answer(
        translator.get("phone_number"),
        reply_markup=common.request_contact(translator.get("phone_number_kb"))
    )


@register_router.message(F.contact, RegisterGroup.phone_number)
async def process_registration(message: Message, state: FSMContext, translator: LocalizedTranslator):
    await state.update_data({
        'phone_number': message.contact.phone_number
    })
    await state.set_state(RegisterGroup.region)
    return await message.answer(
        translator.get("region"),
        reply_markup=common.show_regions()[0]
    )


@register_router.message(F.text.in_(common.show_regions()[1]), RegisterGroup.region)
async def process_registration(message: Message, state: FSMContext, translator: LocalizedTranslator, db: Database):
    await state.update_data({
        'region': message.text
    })
    data = await state.get_data()
    try:
        await db.seller.new(
            user_id=message.from_user.id,
            fullname=data.get("fullname"),
            phone_number=data.get("phone_number"),
            region=data.get("region"),
            language=data.get("language"),
        )
        await db.session.commit()
    except IntegrityError:
        print("User already exists")

    return await message.answer(
        translator.get("category"),
        reply_markup=common.category()
    )