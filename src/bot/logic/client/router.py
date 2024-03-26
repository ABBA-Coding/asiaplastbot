from aiogram import Router

from src.bot.filters.register_filter import ClientFilter

client_router = Router(name='Client')
client_router.message.filter(ClientFilter())