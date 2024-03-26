from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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


def show_regions():
    regions = [
        "Toshkent",
        "Namangan viloyati",
        "Andijon viloyati",
        "Buxoro viloyati",
        "Jizzax viloyati",
        "Qashqadaryo viloyati",
        "Navoi viloyati",
        "Samarqand viloyati",
        "Surxondaryo viloyati",
        "Sirdaryo viloyati",
        "Farg'ona viloyati",
        "Xorazm viloyati",
        "Qoraqalpog'iston Respublikasi",
    ]
    kb = [
        [types.KeyboardButton(text=text)] for text in regions
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
   
    return keyboard, regions


def category():
    kb = [
        [types.KeyboardButton(text="Tovar sotish")],
        # [types.KeyboardButton(text="Mening keshbeklarim")],
        # [types.KeyboardButton(text="Keshbeklar tarixi")],
        [types.KeyboardButton(text="Barcha sotuvlar")],
        [types.KeyboardButton(text="Aloqa")],
        [types.KeyboardButton(text="Feedback")],
        [types.KeyboardButton(text="Sozlamalar")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def client_category():
    kb = [
        [types.KeyboardButton(text="Mening keshbeklarim")],
        [types.KeyboardButton(text="Keshbeklar tarixi")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def confirm():
    kb = [
        [types.KeyboardButton(text="Tasdiqlash")],
        [types.KeyboardButton(text="Bekor qilish")],
        [types.KeyboardButton(text="Menyuga qaytish")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def back_to_menu():
    kb = [
        [types.KeyboardButton(text="Menyuga qaytish")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def cashback_history():
    kb = [
        [types.KeyboardButton(text="Oxirgi 5 kun")],
        [types.KeyboardButton(text="Oxirgi 10 kun")],
        [types.KeyboardButton(text="Oxirgi 30 kun")],
        [types.KeyboardButton(text="Oxirgi 60 kun")],
        [types.KeyboardButton(text="Oxirgi 90 kun")],
        # [types.KeyboardButton(text="Barcha sotuvlar")],
        [types.KeyboardButton(text="Barcha xaridlar")],
        [types.KeyboardButton(text="Menyuga qaytish")],
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
 


def show_settings():
    kb = [
        [types.KeyboardButton(text="Ism o'zgartirish")],
        [types.KeyboardButton(text="Hududni o'zgartirish")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def back_to_settings():
    kb = [
        [types.KeyboardButton(text="Sozlamalarga qaytish")],
        [types.KeyboardButton(text="Menyuga qaytish")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


def admin_dashboard():
    kb = [
        [types.KeyboardButton(text="Sotuvchini qo'shish")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
