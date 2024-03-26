from sqlalchemy.exc import IntegrityError

from aiogram import F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.cache import Cache
from src.configuration import conf
from src.db.database import Database
from src.language.translator import LocaleScheme, LocalizedTranslator
from .router import register_router
from ...structures.fsm.registration import RegisterGroup
from ...structures.keyboards import common
from ...utils.formatters import price_formatter


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
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    db: Database,
    bot: Bot
):
    phone_number = message.contact.phone_number if message.contact.phone_number.startswith('+') else f"+{message.contact.phone_number}"
    await state.update_data({
        'phone_number': phone_number
    })

    data = await state.get_data()
    deep_link = data.get("deep_link")
    allowed_sellers = await db.allowed.get_allowed_sellers()
    seller_id = data.get("seller_id")
    seller = await db.seller.get_me(user_id=seller_id)
    
    if deep_link:
        product = await db.product.get_product_by_check_id(deep_link)
        await db.product.edit(
            check_id=deep_link,
            status=True
        )

        await db.client.add_or_update(
            user_id=message.from_user.id,
            fullname=data.get("fullname"),
            phone_number=data.get("phone_number"),
            language=data.get("language"),
            product_id=data.get("product_id"),
        )

        await db.purchase.new(
            product_id=data.get("product_id"),
            client_id=message.from_user.id,
            region=seller.region,
        )

        logo_path = conf.MEDIA_URL / f"logo/logo.jpg"

        image_from_pc = types.FSInputFile(logo_path)
        logo_img = await message.answer_photo(
            image_from_pc,
            caption=translator.get(
                "congrats", 
                price=price_formatter(product.price),
                check_id=product.check_id
            ),
            reply_markup=types.ReplyKeyboardRemove()
        )

        cashback = data.get("price") / 100
        all_data = await db.cashback.get_cashbacks_by_client_id(client_id=message.from_user.id)
        sum_of_cashbacks = (sum(all_data) + data.get("price")) / 100

        await message.answer(
            f"Keshbek summasiga {price_formatter(cashback)} so'm qo'shildi. "
            f"Hozirda umumiy keshbek summasi: {price_formatter(sum_of_cashbacks)} so'm",
            reply_markup=common.client_category()
        )

        await db.cashback.new(
            price=data.get("price"),
            check_id=product.check_id,
            status=False,
            client_id=message.from_user.id
        )
        
        await db.session.commit()
        return

    elif phone_number not in allowed_sellers:
        return await message.answer(
            translator.get("not_in_sellers"),
            reply_markup = types.ReplyKeyboardRemove()
        )

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
