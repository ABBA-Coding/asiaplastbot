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
        [types.KeyboardButton(text="Mening keshbeklarim")],
        [types.KeyboardButton(text="Keshbeklar tarixi")],
        [types.KeyboardButton(text="Aloqa")],
        [types.KeyboardButton(text="Feedback")],
        [types.KeyboardButton(text="Sozlamalarim")],
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
