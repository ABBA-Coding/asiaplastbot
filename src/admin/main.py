#!/usr/bin/env python3

import uvicorn
from typing import Optional

from fastapi import FastAPI
from sqladmin import Admin

from .auth import AdminAuth
from ..configuration import conf

from ..db.database import create_async_engine
from .views import (
    UserAdmin, SellerAdmin, AllowedSellerAdmin,
    ClientAdmin, ProductAdmin, CashbackAdmin,
)

app = FastAPI()
engine = create_async_engine(conf.db.build_connection_str())
authentication_backend = AdminAuth(secret_key=conf.SECRET_KEY)
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)
admin.add_view(SellerAdmin)
admin.add_view(AllowedSellerAdmin)
admin.add_view(ClientAdmin)
admin.add_view(ProductAdmin)
admin.add_view(CashbackAdmin)


# if __name__ == "__main__":
#     uvicorn.run(app="main:app", reload=True)