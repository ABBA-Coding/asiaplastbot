"""This package is used for a bot logic implementation."""
from .help import help_router
from .start import start_router
from .register import register_router
from .seller import seller_router
from .client import client_router
from .admin import admin_router

routers = (start_router, help_router, register_router, seller_router, client_router, admin_router,)
