from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

# Admin endpoints
@router.get("/admin", response_model=List[schemas.OrderResponse])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[schemas.OrderStatus] = None,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
):
    """
    Retrieve orders (admin only).
    """
    orders = crud.order.get_multi(db, skip=skip, limit=limit, status=status)
    return orders

@router.get("/admin/{order_id}", response_model=schemas.OrderResponse)
def read_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
):
    """
    Get order by ID (admin only).
    """
    order = crud.order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/admin/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    status_in: schemas.OrderStatusUpdate,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
):
    """
    Update order status (admin only).
    """
    order = crud.order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order = crud.order.update_status(db=db, db_obj=order, status=status_in.status)
    return order

# User endpoints
@router.post("/", response_model=schemas.OrderResponse)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: schemas.OrderCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Create new order.
    """
    order = crud.order.create(db=db, obj_in=order_in, user_id=current_user.id)
    return order

@router.get("/", response_model=List[schemas.OrderResponse])
def read_user_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[schemas.OrderStatus] = None,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Retrieve user's orders.
    """
    orders = crud.order.get_multi_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit, status=status
    )
    return orders

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def read_user_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Get user's order by ID.
    """
    order = crud.order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return order 