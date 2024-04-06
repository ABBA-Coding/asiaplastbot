import random
import qrcode

from datetime import datetime, timedelta

from aiogram import Bot
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart

from src.cache import Cache
from src.configuration import conf
from src.db.database import Database
from src.language.translator import LocalizedTranslator
from .router import seller_router
from ...utils.formatters import price_formatter, date_formatter
from ...structures.fsm.category import CategoryGroup, CashbackHistoryGroup, SettingsGroup, FeedbackGroup
from ...structures.keyboards import common


@seller_router.message(CommandStart())
async def restart_handler(
        message: types.Message,
        translator: LocalizedTranslator
):
    await message.answer(
        translator.get("menu"),
        reply_markup=common.category(translator)
    )


@seller_router.message(F.text.in_({"Tovar sotish", "Продажи товаров"}))
async def process_registration(
        message: Message,
        state: FSMContext,
        translator: LocalizedTranslator,
):
    await state.set_state(CategoryGroup.price)

    return await message.answer(
        translator.get("price"),
        reply_markup=common.back_btn(translator)
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
        reply_markup=common.confirm(translator)
    )


@seller_router.message(F.text.in_({
    "Tasdiqlash", "Bekor qilish", "Menyuga qaytish",
    "Вернуться в меню", "Отмена", "Подтверждать"
    }), CategoryGroup.confirm)
async def process_registration(
        message: Message,
        state: FSMContext,
        db: Database,
        translator: LocalizedTranslator,
        bot: Bot
):
    if message.text != translator.get("Tasdiqlash"):
        await message.answer(
            translator.get("category"),
            reply_markup=common.category(translator)
        )
        await state.clear()

    else:
        data = await state.get_data()

        me = await bot.me()
        random_number = random.randint(10000000, 99999999)
        img = qrcode.make(f"https://t.me/{me.username}?start={random_number}")
        img_path = conf.IMAGE_DIR / f"{random_number}.png"
        img.save(str(img_path))

        image_from_pc = FSInputFile(img_path)
        qr_image = await message.answer_photo(
            image_from_pc,
            caption=translator.get(
                    "purchase_check",
                    price = price_formatter(data.get('price')),
                    random_number = random_number  
            ),
            reply_markup=common.back_to_menu(translator)
        )

        # await db.cashback.new(
        #     price=data.get("price"),
        #     check_id=random_number,
        #     status=False,
        #     seller_id=message.from_user.id
        # )
        await db.product.new(
            price=data.get("price"),
            check_id=random_number,
            qr_image_path=str(img_path),
            qr_image_file_id=qr_image.photo[-1].file_id,
            status=False,
            seller_id=message.from_user.id
        )
        await db.session.commit()


@seller_router.message(F.text.in_({"Barcha sotuvlar", "Все покупки"}))
async def process_registration(
        message: Message,
        state: FSMContext,
        translator: LocalizedTranslator,
        db: Database,
):
    products = await db.product.get_sold_products(message.from_user.id)

    if not products:
        return await message.answer(translator.get("not_sold_yet"))

    formatted_data = "\n".join([
        f"{num}. {price_formatter(product.price)} check\nID: {product.check_id}, {date_formatter(str(product.created_at))}"
        for num, product in enumerate(products, start=1)
    ])

    await message.answer(formatted_data)


@seller_router.message(F.text.in_({"Menyuga qaytish", "Вернуться в меню", "Orqaga", "Назад"}))
async def process_registration(
        message: Message,
        state: FSMContext,
        translator: LocalizedTranslator,
):
    await message.answer(
        translator.get("category"),
        reply_markup=common.category(translator)
    )
    await state.clear()


@seller_router.message(F.text.in_({"Aloqa", "Задать вопрос"}))
async def process_registration(
        message: Message,
        state: FSMContext,
        translator: LocalizedTranslator,
):
    return await message.answer(
        translator.get("contacts")
    )


@seller_router.message(F.text.in_({"Feedback", "Обратная связь"}))
async def process_registration(
        message: Message,
        state: FSMContext,
        translator: LocalizedTranslator,
):
    await state.set_state(FeedbackGroup.message)
    return await message.answer(
        translator.get("feedback"),
        reply_markup=common.back_btn()
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
        reply_markup=common.category(translator)
    )
    await state.clear()


@seller_router.message(F.text.in_({"Sozlamalar", "Sozlamalarga qaytish", "Настройки"}))
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
        reply_markup=common.show_settings(translator)
    )


@seller_router.message(F.text.in_({"Ism o'zgartirish", "Изменить имя"}), SettingsGroup.option)
async def process_registration(
        message: Message,
        state: FSMContext,
        translator: LocalizedTranslator,
        db: Database,
):
    await state.set_state(SettingsGroup.name)
    await message.answer(
        translator.get("fullname"),
        reply_markup=common.back_to_settings(translator)
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
        reply_markup=common.category(translator)
    )
    await state.clear()


@seller_router.message(F.text.in_({"Hududni o'zgartirish", "Изменить область"}), SettingsGroup.option)
async def process_registration(
        message: Message,
        state: FSMContext,
        translator: LocalizedTranslator,
        db: Database,
):
    await state.set_state(SettingsGroup.region)
    await message.answer(
        translator.get("region"),
        reply_markup=common.show_regions(translator)[0]
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
        reply_markup=common.category(translator)
    )
    await state.clear()
