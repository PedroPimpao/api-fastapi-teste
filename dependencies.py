from sqlalchemy.orm import sessionmaker, Session
from models import db, Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM
from main import oauth2_schema

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
    
def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        userId = int(dic_info.get('sub'))
    except JWTError:
        raise HTTPException(status_code=401, detail="Access Denied")
    user = session.query(Usuario).filter(Usuario.id == userId).first()
    if not user:
        raise HTTPException(status_code=401, detail="Access Denied")
    return user






















