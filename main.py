from fastapi import FastAPI


app = FastAPI()

from routes.auth_routes import auth_router
from routes.order_routes import order_router

# app.get("/")(lambda: {"message": "Hello World"})
app.include_router(auth_router)
app.include_router(order_router)









