#!/usr/bin/env python3

from fastapi import FastAPI
from sqladmin import Admin

from .auth import AdminAuth
from .settings import engine
from ..configuration import conf

from .views import (
    UserAdmin, SellerAdmin, AllowedSellerAdmin,
    ClientAdmin, ProductAdmin, CashbackAdmin, 
    ReportView, PurchaseAdmin, FeedbackAdmin, 
)

app = FastAPI()
authentication_backend = AdminAuth(secret_key=conf.SECRET_KEY)
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend, templates_dir='src/admin/templates')


admin.add_view(UserAdmin)
admin.add_view(SellerAdmin)
admin.add_view(AllowedSellerAdmin)
admin.add_view(ClientAdmin)
admin.add_view(ProductAdmin)
admin.add_view(CashbackAdmin)
admin.add_view(PurchaseAdmin)
admin.add_view(FeedbackAdmin)
admin.add_view(ReportView)
