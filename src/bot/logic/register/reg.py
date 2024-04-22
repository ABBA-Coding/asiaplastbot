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
    
    if deep_link:
        try:
            product = await db.product.get_product_by_check_id(deep_link)
            seller = await db.seller.get_me(user_id=product.seller_id)
        except AttributeError:
            await state.set_state(RegisterGroup.receive_cashback_id)
            return await message.answer(
                translator.get("send_cashback_code"),
                reply_markup=types.ReplyKeyboardRemove()
            )
    
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
            product_id=product.id,
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

        cashback = (product.price / 100) * 4
        all_data = await db.cashback.get_cashbacks_by_client_id(client_id=message.from_user.id)
        sum_of_cashbacks = ((sum(all_data) + product.price) / 100) * 4

        await message.answer(
            translator.get(
                "cashback_info",
                price=price_formatter(cashback),
                sum_of_cashbacks=price_formatter(sum_of_cashbacks)
            ),
            reply_markup=common.client_category(translator)
        )

        await db.cashback.new(
            price=product.price,
            check_id=product.check_id,
            status=False,
            client_id=message.from_user.id
        )
        
        await db.session.commit()
        await state.clear()

    elif phone_number in allowed_sellers:
        await state.set_state(RegisterGroup.region)
        return await message.answer(
            translator.get("region"),
            reply_markup=common.show_regions(translator)[0]
        )

    else:
        await state.set_state(RegisterGroup.receive_cashback_id)
        return await message.answer(
            translator.get("send_cashback_code"), 
            reply_markup=types.ReplyKeyboardRemove()
        )


@register_router.message(RegisterGroup.receive_cashback_id)
async def process_registration(message: Message, state: FSMContext, translator: LocalizedTranslator, db: Database):
    data = await state.get_data()

    try:
        cleaned_string = message.text.replace('\u2068', '').replace('\u2069', '')
        cashback_id = int(cleaned_string)

        product = await db.product.get_product_by_check_id(cashback_id)
        seller = await db.seller.get_me(user_id=product.seller_id)
    except (AttributeError, ValueError):
        return await message.answer(translator.get("incorrect_id"))


    try:
        await db.client.add_or_update(
            user_id=message.from_user.id,
            fullname=data.get("fullname"),
            phone_number=data.get("phone_number"),
            language=data.get("language"),
            product_id=product.id,
        )

        await db.cashback.new(
            price=product.price,
            check_id=product.check_id,
            status=False,
            client_id=message.from_user.id
        )

        await db.purchase.new(
            product_id=product.id,
            client_id=message.from_user.id,
            region=seller.region,
        )

        await db.product.edit(
            check_id=cashback_id,
            status=True
        )
    except Exception as e:
        print(e)
        return message.answer(
            translator.get("already_purchased")
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

    cashback = (product.price / 100) * 4
    all_data = await db.cashback.get_cashbacks_by_client_id(client_id=message.from_user.id)
    sum_of_cashbacks = ((sum(all_data) + product.price) / 100) * 4

    await message.answer(
        translator.get(
            "cashback_info",
            price=price_formatter(cashback),
            sum_of_cashbacks=price_formatter(sum_of_cashbacks)
        ),
        reply_markup=common.client_category(translator)
    )
    
    await db.session.commit()
    await state.clear()
    

@register_router.message(RegisterGroup.region)
async def process_registration(message: Message, state: FSMContext, translator: LocalizedTranslator, db: Database):
    if message.text not in common.show_regions(translator)[1]:
        return await message.answer(translator.get("choose_from_list"))

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
        reply_markup=common.category(translator)
    )
