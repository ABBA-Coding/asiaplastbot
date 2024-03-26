import random, qrcode

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

from aiogram import Bot
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart


from src.cache import Cache
from src.configuration import conf
from src.db.database import Database
from src.language.translator import LocaleScheme, LocalizedTranslator
from src.bot.filters.register_filter import ClientFilter
from .router import client_router
from ...utils.formatters import price_formatter, date_formatter
from ...structures.fsm.category import CategoryGroup, CashbackHistoryGroup, SettingsGroup, FeedbackGroup
from ...structures.keyboards import common


@client_router.message(CommandStart())
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    db: Database,
    bot: Bot
):
    texts = message.text.split()
    check_id = int(texts[1]) if len(texts) == 2 else None
    product = await db.product.get_product_by_check_id(check_id)

    cashback = await db.cashback.get_cashback_by_client_id_and_check_id(message.from_user.id, check_id)
    if cashback:
        return message.answer("Siz ushbu tovarni harid qilgansiz")

    if check_id:
        seller_id = product.seller_id
        seller = await db.seller.get_me(user_id=seller_id)

        await db.product.edit(
            check_id=check_id,
            status=True
        )

        await db.purchase.new(
            product_id=product.id,
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

        cashback = product.price / 100
        all_data = await db.cashback.get_cashbacks_by_client_id(client_id=message.from_user.id)
        sum_of_cashbacks = (sum(all_data) + product.price) / 100

        await message.answer(
            f"Keshbek summasiga {price_formatter(cashback)} so'm qo'shildi. "
            f"Hozirda umumiy keshbek summasi: {price_formatter(sum_of_cashbacks)} so'm",
            reply_markup=common.client_category()
        )

        await db.cashback.new(
            price=product.price,
            check_id=product.check_id,
            status=False,
            client_id=message.from_user.id
        )
        
        await db.session.commit()
        return

    else:
        await message.answer(
            translator.get("menu"),
            reply_markup=common.client_category()
        )
        
    await state.clear()


@client_router.message(F.text=="Mening keshbeklarim")
async def process_registration(
    message: Message, 
    translator: LocalizedTranslator,
    db: Database
):
    all_data = await db.cashback.get_cashbacks_by_client_id(client_id=message.from_user.id)
    sum_of_cashbacks = sum(all_data) / 100

    return await message.answer(
        translator.get("sum_of_cashback", price=price_formatter(sum_of_cashbacks))
    )


@client_router.message(F.text=="Keshbeklar tarixi")
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


@client_router.message(CashbackHistoryGroup.step1)
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

    elif message.text == "Barcha xaridlar":
        cashbacks = await db.cashback.get_last_cashbacks(message.from_user.id)
        formatted_data = "\n".join([
            f"{num}. {price_formatter(cashback.price)} chek\nID: {cashback.check_id}, {date_formatter(str(cashback.created_at))}" 
                for num, cashback in enumerate(cashbacks, start=1)
        ])
        await message.answer(formatted_data) 
    
    elif message.text == "Menyuga qaytish":
        await message.answer(
            translator.get("category"),
            reply_markup=common.client_category()
        )
        await state.clear()


@client_router.message(F.text=="Menyuga qaytish")
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    await message.answer(
        translator.get("category"),
        reply_markup=common.client_category()
    )
    await state.clear()
