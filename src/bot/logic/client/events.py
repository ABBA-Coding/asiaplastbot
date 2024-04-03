from datetime import datetime, timedelta

from aiogram import Bot
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.configuration import conf
from src.db.database import Database
from src.language.translator import LocalizedTranslator
from .router import client_router
from ...utils.formatters import price_formatter, date_formatter
from ...structures.fsm.category import CashbackHistoryGroup
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
        return message.answer(translator.get("purchased"))

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
        return

    else:
        await message.answer(
            translator.get("menu"),
            reply_markup=common.client_category(translator)
        )
        
    await state.clear()


@client_router.message(F.text.in_({"Mening keshbeklarim", "Мои кэшбэки"}))
async def process_registration(
    message: Message, 
    translator: LocalizedTranslator,
    db: Database
):
    all_data = await db.cashback.get_cashbacks_by_client_id(client_id=message.from_user.id)
    sum_of_cashbacks = (sum(all_data) / 100) * 4

    return await message.answer(
        translator.get("sum_of_cashback", price=price_formatter(sum_of_cashbacks))
    )


@client_router.message(F.text.in_({"Keshbeklar tarixi", "История кэшбэков"}))
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    await state.set_state(CashbackHistoryGroup.step1)
    return await message.answer(
        translator.get("cashback_history_period"),
        reply_markup=common.cashback_history(translator)
    )


@client_router.message(CashbackHistoryGroup.step1)
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
    db: Database,
):
    delta = lambda x: datetime.utcnow() - timedelta(days=x)
    
    target = translator.get("last")
    if message.text.startswith(target) and len(message.text.split()) == 3:
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

    elif message.text == translator.get("Barcha_xaridlar"):
        cashbacks = await db.cashback.get_last_cashbacks(message.from_user.id)
        formatted_data = "\n".join([
            f"{num}. {price_formatter(cashback.price)} chek\nID: {cashback.check_id}, {date_formatter(str(cashback.created_at))}" 
                for num, cashback in enumerate(cashbacks, start=1)
        ])
        await message.answer(formatted_data) 
    
    elif message.text == translator.get("Menyuga_qaytish") or message.text == translator.get("back"):
        await message.answer(
            translator.get("category"),
            reply_markup=common.client_category(translator)
        )
        await state.clear()


@client_router.message(F.text.in_({"Menyuga qaytish", "Вернуться в меню", "Orqaga", "Назад"}))
async def process_registration(
    message: Message, 
    state: FSMContext, 
    translator: LocalizedTranslator,
):
    await message.answer(
        translator.get("category"),
        reply_markup=common.client_category(translator)
    )
    await state.clear()
