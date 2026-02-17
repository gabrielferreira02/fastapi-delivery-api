from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/images", StaticFiles(directory="app/uploads/images"), name="images")

from app.api.routes.auth_routes import auth_router
from app.api.routes.user_routes import user_router
from app.api.routes.category_routes import category_router
from app.api.routes.product_routes import product_router
from app.api.routes.order_routes import order_router

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(order_router)