from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from src.language.translator import LocalizedTranslator


def show_languages():
    kb = [
        [types.KeyboardButton(text="🇺🇿 O'zbek")],
        [types.KeyboardButton(text="🇷🇺 Русский")],
        # [types.KeyboardButton(text="English")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def request_contact(text):
    kb = [
        [types.KeyboardButton(text=text, request_contact=True)],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def show_regions(translator: LocalizedTranslator):
    regions = [
        "Toshkent",
        "Namangan_viloyati",
        "Andijon_viloyati",
        "Buxoro_viloyati",
        "Jizzax_viloyati",
        "Qashqadaryo_viloyati",
        "Navoi_viloyati",
        "Samarqand_viloyati",
        "Surxondaryo_viloyati",
        "Sirdaryo_viloyati",
        "Fargona_viloyati",
        "Xorazm_viloyati",
        "Qoraqalpogiston_Respublikasi",
    ]

    translated = [translator.get(region) for region in regions]

    kb = [
        [types.KeyboardButton(text=text)] for text in translated
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
   
    return keyboard, translated


def category(translator: LocalizedTranslator):
    kb = [
        [types.KeyboardButton(text=translator.get("Tovar_sotish"))],
        # [types.KeyboardButton(text="Mening keshbeklarim")],
        # [types.KeyboardButton(text="Keshbeklar tarixi")],
        [types.KeyboardButton(text=translator.get("Barcha_sotuvlar"))],
        [types.KeyboardButton(text=translator.get("Aloqa"))],
        [types.KeyboardButton(text=translator.get("Feedback"))],
        [types.KeyboardButton(text=translator.get("Sozlamalar"))],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def client_category(translator: LocalizedTranslator):
    kb = [
        [types.KeyboardButton(text=translator.get("Mening_keshbeklarim"))],
        [types.KeyboardButton(text=translator.get("Keshbeklar_tarixi"))],
        [types.KeyboardButton(text=translator.get("Keshbek_id"))],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def confirm(translator: LocalizedTranslator):
    kb = [
        [types.KeyboardButton(text=translator.get("Tasdiqlash"))],
        [types.KeyboardButton(text=translator.get("Bekor_qilish"))],
        [types.KeyboardButton(text=translator.get("Menyuga_qaytish"))],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def back_to_menu(translator: LocalizedTranslator):
    kb = [
        [types.KeyboardButton(text=translator.get("Menyuga_qaytish"))],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def back_btn(translator):
    kb = [
        [types.KeyboardButton(text=translator.get("back"))],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def cashback_history(translator: LocalizedTranslator):
    kb = [
        [types.KeyboardButton(text=translator.get("Oxirgi_5_kun"))],
        [types.KeyboardButton(text=translator.get("Oxirgi_10_kun"))],
        [types.KeyboardButton(text=translator.get("Oxirgi_30_kun"))],
        [types.KeyboardButton(text=translator.get("Oxirgi_60_kun"))],
        [types.KeyboardButton(text=translator.get("Oxirgi_90_kun"))],
        # [types.KeyboardButton(text="Barcha sotuvlar")],
        [types.KeyboardButton(text=translator.get("Barcha_xaridlar"))],
        [types.KeyboardButton(text=translator.get("Menyuga_qaytish"))],
        [types.KeyboardButton(text=translator.get("back"))],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


# def show_sells():
#     kb = [
#         [types.KeyboardButton(text="Oxirgi 5 kun")],
#         [types.KeyboardButton(text="Oxirgi 10 kun")],
#         [types.KeyboardButton(text="Oxirgi 30 kun")],
#         [types.KeyboardButton(text="Oxirgi 60 kun")],
#         [types.KeyboardButton(text="Oxirgi 90 kun")],
#         [types.KeyboardButton(text="Barcha sotuvlar")],
#         [types.KeyboardButton(text="Barcha xaridlar")],
#         [types.KeyboardButton(text="Menyuga qaytish")],
#     ]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

#     return keyboard
 


def show_settings(translator: LocalizedTranslator):
    kb = [
        [types.KeyboardButton(text=translator.get("Ism_ozgartirish"))],
        [types.KeyboardButton(text=translator.get("Hududni_ozgartirish"))],
        [types.KeyboardButton(text=translator.get("back"))],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def back_to_settings(translator: LocalizedTranslator):
    kb = [
        [types.KeyboardButton(text=translator.get("Sozlamalarga_qaytish"))],
        [types.KeyboardButton(text=translator.get("Menyuga_qaytish"))],
        [types.KeyboardButton(text=translator.get("back"))],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def admin_dashboard():
    kb = [
        [types.KeyboardButton(text="Sotuvchini qo'shish")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
