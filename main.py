from fastapi import FastAPI
from passlib.context import CryptContext
from config import SECRET_KEY
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl = 'auth/login-form')

from routes.auth_routes import auth_router
from routes.order_routes import order_router

# app.get("/")(lambda: {"message": "Hello World"})
app.include_router(auth_router)
app.include_router(order_router)









