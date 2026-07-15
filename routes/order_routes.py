from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session
from schemas import OrderSchema
from models import Pedidos

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def orders_home():
    """
    Rota de pedidos
    """

@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Pedidos(usuario=order_schema.usuario)
    session.add(new_order)
    session.commit()
    return {"message": f"Pedido criado com sucesso. ID do Pedido: {new_order.id}"}