from fastapi import Request
from sqlalchemy import select, func
from sqladmin import ModelView, BaseView, expose

from .settings import Session

from ..db.models import (
    User, Seller, AllowedSeller, 
    Client, Product, Cashback, 
    Purchase, Feedback,
)



class UserAdmin(ModelView, model=User):
    column_list = [User.user_id, User.user_name, User.first_name, User.second_name]
    can_create = False
    can_edit = False
    can_delete = False
    icon = "fa-solid fa-users"
    name_plural = "Foydalanuvchilar"
    page_size = 100
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class SellerAdmin(ModelView, model=Seller):
    column_list = [
        Seller.fullname, Seller.phone_number,
        Seller.language, Seller.products, 
        Seller.created_at
    ]
    column_searchable_list = [Seller.fullname]
    can_create = False
    can_delete = False
    icon = "fa-solid fa-users"
    name_plural = "Sotuvchilar"
    page_size = 100
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True

   
class AllowedSellerAdmin(ModelView, model=AllowedSeller):
    column_list = [
        AllowedSeller.phone_number,
    ]
    column_searchable_list = [AllowedSeller.phone_number]

    icon = "fa-solid fa-user-plus"
    name_plural = "Sotuvchi qo'shish"
    page_size = 100
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True

   
class ClientAdmin(ModelView, model=Client):
    column_list = [
        Client.fullname, Client.phone_number, 
        Client.created_at
    ]
    column_searchable_list = [Client.fullname]
    
    icon = "fa-solid fa-users"
    name_plural = "Klientlar"
    page_size = 100
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class ProductAdmin(ModelView, model=Product):
    column_list = [
        "formatted_price", Product.status,
        "seller_phone_number",
        Product.seller, Product.created_at,
    ]

    column_details_list = [
        Product.price, Product.status,
        "seller_phone_number",
        Product.seller, Product.created_at,
    ]

    icon = "fa-solid fa-store"
    name_plural = "Tovarlar"
    page_size = 100
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True
    

class PurchaseAdmin(ModelView, model=Purchase):
    column_list = [
        Purchase.product, Purchase.client, Purchase.region
    ]
    icon = "fa-solid fa-cart-shopping"
    name_plural = "Haridlar"
    page_size = 100
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class CashbackAdmin(ModelView, model=Cashback):
    column_list = [
        "formatted_price", "cashback_sum", 
        Cashback.status, "client_phone_number",
        Cashback.client, Cashback.created_at, 
    ]
    
    can_create = False
    icon = "fa-solid fa-money-check-dollar"
    name_plural = "Keshbeklar"
    page_size = 100
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class FeedbackAdmin(ModelView, model=Feedback):
    column_list = [
        Feedback.message, Feedback.user,
    ]

    icon = "fa-solid fa-comment"
    name_plural = "Fikrlar"
    page_size = 100
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class ReportView(BaseView):
    name = "Hisobot"
    icon = "fa-solid fa-chart-line"

    @expose("/report", methods=["GET"])
    async def report_page(self, request):
        async with Session(expire_on_commit=False) as session:
            stmt = select(Purchase.region, func.count().label('region_count')).group_by(Purchase.region)
            result = await session.execute(stmt)
            rows = result.fetchall()

            stmt = select(func.count(Purchase.region))
            result = await session.execute(stmt)
            region_count = result.scalar_one()

            regions = [{'name': n, 'count': c} for n, c in rows]

        return await self.templates.TemplateResponse(
            request,
            "report.html",
            context={
                "regions": regions,
                "region_count": region_count,
            },
        )
