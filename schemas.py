from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

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

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
    
class OrderItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    amount: int = Field(validation_alias="quantidade")
    flavor: str = Field(validation_alias="sabor")
    size: str = Field(validation_alias="tamanho")
    unit_price: float = Field(validation_alias="preco_unitario")

class ResponseOrderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    preco: float
    itens: List[OrderItemSchema]
