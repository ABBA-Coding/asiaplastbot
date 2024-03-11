import random, qrcode

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

from aiogram import Bot
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile

from src.cache import Cache
from src.configuration import conf
from src.db.database import Database
from src.language.translator import LocaleScheme, LocalizedTranslator
from .router import seller_router
from ...utils.formatters import price_formatter, date_formatter
from ...structures.fsm.category import CategoryGroup, CashbackHistoryGroup, SettingsGroup, FeedbackGroup
from ...structures.keyboards import common


@seller_router.message(F.text=="Tovar sotish")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    await state.set_state(CategoryGroup.price)

    return await message.answer(
        translator.get("price"),
        reply_markup=types.ReplyKeyboardRemove()
    )


@seller_router.message(F.text.isdigit(), CategoryGroup.price)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):

    await state.update_data({
        'price': int(message.text),
    })
    await state.set_state(CategoryGroup.confirm)

    return await message.answer(
        f"{price_formatter(int(message.text))} {translator.get('confirm')}",
        reply_markup=common.confirm()
    )


@seller_router.message(F.text.in_({"Tasdiqlash", "Bekor qilish", "Menyuga qaytish"}), CategoryGroup.confirm)
async def process_registration(
    message: Message, 
    state: FSMContext,
    db: Database,
    translator: LocalizedTranslator,
    bot: Bot
):
    if message.text != "Tasdiqlash":
        await message.answer(
            "Kategoriyani tanlang",
            reply_markup=common.category()
        )
        await state.clear()

    else:
        data = await state.get_data()

        me = await bot.me()
        random_number = random.randint(10000000, 99999999)
        img = qrcode.make(f"https://t.me/{me.username}?start={random_number}")
        img_path = conf.MEDIA_URL / f"images/{random_number}.png"
        img.save(str(img_path))

        image_from_pc = FSInputFile(img_path)
        qr_image = await message.answer_photo(
            image_from_pc,
            caption=f"{price_formatter(data.get('price'))} so'mlik xarid cheki\n"
                    f"ID: {random_number}",
            reply_markup=common.back_to_menu()
        )

        await db.cashback.new(
            price=data.get("price"),
            check_id=random_number,
            status=False,
            seller_id=message.from_user.id
        )
        await db.product.new(
            price=data.get("price"),
            check_id=random_number,
            qr_image_path=str(img_path),
            qr_image_file_id=qr_image.photo[-1].file_id,
            status=False,
            seller_id=message.from_user.id
        )
        await db.session.commit()

        all_data = await db.cashback.get_cashbacks_by_seller_id(seller_id=message.from_user.id)


@seller_router.message(F.text=="Mening keshbeklarim")
async def process_registration(
    message: Message, 
    translator: LocalizedTranslator,
    db: Database
):
    all_data = await db.cashback.get_cashbacks_by_seller_id(seller_id=message.from_user.id)
    sum_of_cashbacks = sum(all_data) / 100

    return await message.answer(
        translator.get("sum_of_cashback", price=price_formatter(sum_of_cashbacks))
    )


@seller_router.message(F.text=="Keshbeklar tarixi")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    await state.set_state(CashbackHistoryGroup.step1)
    return await message.answer(
        translator.get("cashback_history_period"),
        reply_markup=common.cashback_history()
    )


@seller_router.message(CashbackHistoryGroup.step1)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    db: Database,
):
    delta = lambda x: datetime.utcnow() - timedelta(days=x)
    
    # TODO add check for empty list
    if message.text.startswith("Oxirgi") and len(message.text.split()) == 3:
        words = message.text.split()
        if words[1].isdigit():
            x_days_ago = delta(int(words[1]))
            cashbacks = await db.cashback.get_last_cashbacks(message.from_user.id, x_days_ago)

            if not cashbacks:
                return await message.answer(translator.get("no_cashbacks"))
            
            formatted_data = "\n".join([
                f"{num}. {price_formatter(cashback.price)} chek\nID: {cashback.check_id}, {date_formatter(str(cashback.created_at))}" 
                    for num, cashback in enumerate(cashbacks, start=1)
            ])
            print("len cashbacks: ", len(cashbacks))
            await message.answer(formatted_data) 

    elif message.text == "Barcha sotuvlar":
        products = await db.product.get_sold_products(message.from_user.id)

        if not products:
            return await message.answer(translator.get("not_sold_yet"))
        
        formatted_data = "\n".join([
            f"{num}. {price_formatter(product.price)} chek\nID: {product.check_id}, {date_formatter(str(product.created_at))}" 
                for num, product in enumerate(products, start=1)
        ])
        await message.answer(formatted_data) 

    elif message.text == "Barcha xaridlar":
        cashbacks = await db.cashback.get_last_cashbacks(message.from_user.id)
        formatted_data = "\n".join([
            f"{num}. {price_formatter(cashback.price)} chek\nID: {cashback.check_id}, {date_formatter(str(cashback.created_at))}" 
                for num, cashback in enumerate(cashbacks, start=1)
        ])
        print("len cashbacks: ", len(cashbacks))
        await message.answer(formatted_data) 
    
    elif message.text == "Menyuga qaytish":
        await message.answer(
            translator.get("category"),
            reply_markup=common.category()
        )
        await state.clear()

@seller_router.message(F.text=="Menyuga qaytish")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    await message.answer(
        translator.get("category"),
        reply_markup=common.category()
    )
    await state.clear()


@seller_router.message(F.text=="Aloqa")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    return await message.answer(
        translator.get("contacts")
    )


@seller_router.message(F.text=="Feedback")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    await state.set_state(FeedbackGroup.message)
    return await message.answer(
        translator.get("feedback"),
        reply_markup=types.ReplyKeyboardRemove()
    )


@seller_router.message(FeedbackGroup.message)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    db: Database,
):
    await db.feedback.new(
        message=message.text,
        user_id=message.from_user.id,
    )
    await db.session.commit()

    await message.answer(
        translator.get("thank_you_for_feedback"),
        reply_markup=common.category()
    )
    await state.clear()


@seller_router.message(F.text.in_({"Sozlamalar", "Sozlamalarga qaytish"}))
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    db: Database,
):
    await state.set_state(SettingsGroup.option)

    me = await db.seller.get_me(message.from_user.id)
    return await message.answer(
        translator.get("seller_info", fullname=me.fullname, region=me.region),
            reply_markup=common.show_settings()
    )


@seller_router.message(F.text == "Ism o'zgartirish", SettingsGroup.option)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    db: Database,
):
    await state.set_state(SettingsGroup.name)
    await message.answer(
        translator.get("fullname"),
        reply_markup=common.back_to_settings()
    )


@seller_router.message(SettingsGroup.name)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    db: Database,
):
    await db.seller.edit(
        user_id=message.from_user.id,
        fullname=message.text
    )
    await db.session.commit()

    await message.answer(
        translator.get("name_changed"),
        reply_markup=common.category()
    )
    await state.clear()


@seller_router.message(F.text == "Hududni o'zgartirish", SettingsGroup.option)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    db: Database,
):
    await state.set_state(SettingsGroup.region)
    await message.answer(
        translator.get("region"),
        reply_markup=common.show_regions()[0]
    )


@seller_router.message(SettingsGroup.region)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    db: Database,
):
    await db.seller.edit(
        user_id=message.from_user.id,
        region=message.text
    )
    await db.session.commit()

    await message.answer(
        translator.get("region_changed"),
        reply_markup=common.category()
    )
    await state.clear()
