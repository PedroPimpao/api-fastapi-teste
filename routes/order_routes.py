from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas import OrderSchema, OrderItemSchema
from models import Pedidos, Usuario, ItemPedido

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)])

authorization_error_message = 'You don`t have permission to do this action'

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

@order_router.post("/order/cancel/{orderId}")
async def cancel_order(orderId: int, session: Session = Depends(get_session), user: Usuario = Depends(verify_token)):
    order = session.query(Pedidos).filter(Pedidos.id == orderId).first()
    if not user.admin and user.id != order.usuario:
        raise HTTPException(status_code=401, detail=authorization_error_message)
    if not order:
        raise HTTPException(status_code=400, detail='Order not found')
    order.status = 'CANCELADO'
    session.commit()
    return {
        "message": f"Pedido {order.id} cancelado com sucesso",
        "order": order
    }

@order_router.get('/list')
async def list_orders(session: Session = Depends(get_session), user: Usuario = Depends(verify_token)):
    if not user.admin:
        raise HTTPException(status_code=401, detail=authorization_error_message)
    else: 
        orders = session.query(Pedidos).all()
        return {
            "orders": orders
        }

@order_router.post('/order/add-item/{orderId}')
async def add_item(orderId: int, orderItemSchema: OrderItemSchema, session: Session = Depends(get_session), user: Usuario = Depends(verify_token)):
    order = session.query(Pedidos).filter(Pedidos.id == orderId).first()
    if not order:
        raise HTTPException(status_code=400, detail='Order not found')
    if not user.admin and user.id != order.usuario:
        raise HTTPException(status_code=401, detail=authorization_error_message)
    order_item = ItemPedido(orderItemSchema.amount, orderItemSchema.flavor, orderItemSchema.size, orderItemSchema.unit_price, orderId)
    session.add(order_item)
    order.calcular_preco()
    session.commit()
    return {
        "message": "Item added successfully",
        "item_id": order_item.id,
        "order_price": order.preco
    }

@order_router.post('/order/remove-item/{orderItemId}')
async def remove_item(orderItemId: int, session: Session = Depends(get_session), user: Usuario = Depends(verify_token)):
    orderItem = session.query(ItemPedido).filter(ItemPedido.id == orderItemId).first()

    if not orderItem:
        raise HTTPException(status_code=400, detail='Item not found')

    order = session.query(Pedidos).filter(Pedidos.id == orderItem.pedido).first()

    if not order:
        raise HTTPException(status_code=400, detail='Order not found')
    
    if not user.admin and user.id != order.usuario:
        raise HTTPException(status_code=401, detail=authorization_error_message)
    
    session.delete(orderItem)
    order.calcular_preco()
    session.commit()
    return {
        "message": "Item removed successfully",
        "order_itens": order.itens,
        "order": order
    }

@order_router.post("/order/finish/{orderId}")
async def finish_order(orderId: int, session: Session = Depends(get_session), user: Usuario = Depends(verify_token)):
    order = session.query(Pedidos).filter(Pedidos.id == orderId).first()
    if not user.admin and user.id != order.usuario:
        raise HTTPException(status_code=401, detail=authorization_error_message)
    if not order:
        raise HTTPException(status_code=400, detail='Order not found')
    order.status = 'FINALIZADO'
    session.commit()
    return {
        "message": f"Pedido {order.id} finalizado com sucesso",
        "order": order
    }

@order_router.get('/order/{ordeId}')
async def get_order(orderId: int, session: Session = Depends(get_session), user: Usuario = Depends(verify_token)):
    order = session.query(Pedidos).filter(Pedidos.id == orderId).first()
    if not user.admin and user.id != order.usuario:
        raise HTTPException(status_code=401, detail=authorization_error_message)
    if not order:
        raise HTTPException(status_code=400, detail='Order not found')
    return {
        "message": f"Pedido {order.id} encontrado com sucesso",
        "order": order,
        "itens": order.itens
    }

@order_router.get('/list/{userId}')
async def list_user_orders(userId: int, session: Session = Depends(get_session), user: Usuario = Depends(verify_token)):
    orders = session.query(Pedidos).filter(Pedidos.usuario == userId).all()
    if not user.admin and user.id != userId:
        raise HTTPException(status_code=401, detail=authorization_error_message)
    else: 
        return {
            "orders": orders
        }
