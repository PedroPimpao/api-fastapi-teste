from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

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