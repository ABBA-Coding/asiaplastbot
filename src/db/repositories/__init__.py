"""Repositories module."""
from .abstract import Repository
from .user import UserRepo
from .seller import SellerRepo
from .client import ClientRepo
from .product import ProductRepo
from .cashback import CashbackRepo
from .allowed import AllowedRepo


__all__ = ('UserRepo', 'SellerRepo', 'ClientRepo', 'ProductRepo', 'CashbackRepo', 'Repository', 'AllowedRepo',)
