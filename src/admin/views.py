from fastapi import Request
from sqladmin import ModelView

from ..db.models import (
    User, Seller, AllowedSeller, 
    Client, Product, Cashback,
)


class UserAdmin(ModelView, model=User):
    column_list = [User.user_id, User.user_name, User.first_name, User.second_name]
    can_create = False
    can_edit = False
    can_delete = False
    icon = "fa-solid fa-users"
    name_plural = "Foydalanuvchilar"
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class SellerAdmin(ModelView, model=Seller):
    column_list = [
        Seller.fullname, Seller.phone_number,
        Seller.phone_number, Seller.language, 
        Seller.products, Seller.created_at
    ]
    icon = "fa-solid fa-users"
    name_plural = "Sotuvchilar"
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True

   
class AllowedSellerAdmin(ModelView, model=AllowedSeller):
    column_list = [
        AllowedSeller.phone_number,
    ]
    icon = "fa-solid fa-user-plus"
    name_plural = "Sotuvchi qo'shish"
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True

   
class ClientAdmin(ModelView, model=Client):
    column_list = [
        Client.fullname, Client.phone_number, 
        Client.product_id, Client.created_at
    ]
    icon = "fa-solid fa-users"
    name_plural = "Klientlar"
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.price, Product.check_id,
        Product.seller_id, Product.status,
        Product.created_at,
    ]
    icon = "fa-solid fa-store"
    name_plural = "Tovarlar"
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class CashbackAdmin(ModelView, model=Cashback):
    column_list = [
        Cashback.price, Cashback.check_id,
        Cashback.seller_id, Cashback.status,
        Cashback.seller, Cashback.created_at
    ]

    icon = "fa-solid fa-money-check-dollar"
    name_plural = "Keshbeklar"
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True
