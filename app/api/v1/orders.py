from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate, OrderItemCreate
from app.crud import order as order_crud

router = APIRouter()

@router.get("/", response_model=List[OrderResponse])
async def get_orders(db: Session = Depends(get_db)):
    """Get list of all orders"""
    return order_crud.get_orders(db)

@router.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order"""
    return order_crud.create_order(db, order)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order by ID"""
    order = order_crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    """Update an order"""
    updated_order = order_crud.update_order(db, order_id, order)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order"""
    if not order_crud.delete_order(db, order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

# Order Items endpoints
@router.post("/{order_id}/items", response_model=OrderResponse)
async def add_order_item(
    order_id: int,
    item: OrderItemCreate,
    db: Session = Depends(get_db)
):
    """Add an item to an order"""
    updated_order = order_crud.add_order_item(db, order_id, item)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/{order_id}/items/{item_id}", response_model=OrderResponse)
async def remove_order_item(
    order_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    """Remove an item from an order"""
    updated_order = order_crud.remove_order_item(db, order_id, item_id)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order or item not found")
    return updated_order
