from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(user_id, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire_date = datetime.now(timezone.utc) + token_duration
    dic_info = { "sub": str(user_id), "exp": expire_date }
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token, session: Session = Depends(get_session)):
    user = session.query(Usuario).filter(Usuario.id ==3).first()
    return user

def auth_user(email, password, session):
    user = session.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.senha):
        return False
    
    return user


@auth_router.get('/')
async def home():
    """
    Essa é a rota padrão de autenticação do sistema.
    """
    return {"message": "Home Auth Route"}

@auth_router.post("/create-account")
async def create_account(user_schema: UserSchema, session: Session = Depends(get_session)):

    user = session.query(Usuario).filter(Usuario.email == user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        hashed_password = bcrypt_context.hash(user_schema.password)
        new_user = Usuario(nome=user_schema.name, email=user_schema.email, senha=hashed_password, ativo=user_schema.ativo, admin=user_schema.admin)
        session.add(new_user)
        session.commit()
        return {"message": f"Account created successfully {new_user.email}"}


@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    """
    Rota login
    """
    user = auth_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or invalid credentials")
    else: 
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_duration=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    
@auth_router.get('/refresh-token')
async def use_refresh_token(token):
    user = verify_token(token)
    access_token = create_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }