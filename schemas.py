from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class Config: 
        from_attributes = True

class OrderSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True