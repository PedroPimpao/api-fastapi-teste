from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/list")
async def list_orders():
    return {"message": "List of orders"}