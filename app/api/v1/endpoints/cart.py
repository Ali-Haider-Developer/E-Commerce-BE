from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=schemas.CartResponse)
def read_cart(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Get user's cart.
    """
    cart = crud.cart.get_or_create(db=db, user_id=current_user.id)
    return cart

@router.post("/items", response_model=schemas.CartResponse)
def add_to_cart(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.CartItemCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Add item to cart.
    """
    cart = crud.cart.get_or_create(db=db, user_id=current_user.id)
    cart = crud.cart.add_item(db=db, cart=cart, item_in=item_in)
    return cart

@router.put("/items/{item_id}", response_model=schemas.CartResponse)
def update_cart_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    item_in: schemas.CartItemUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Update cart item.
    """
    cart = crud.cart.get_by_user(db=db, user_id=current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart = crud.cart.update_item(db=db, cart=cart, item_id=item_id, item_in=item_in)
    return cart

@router.delete("/items/{item_id}", response_model=schemas.CartResponse)
def remove_from_cart(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Remove item from cart.
    """
    cart = crud.cart.get_by_user(db=db, user_id=current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart = crud.cart.remove_item(db=db, cart=cart, item_id=item_id)
    return cart

@router.delete("/", response_model=schemas.CartResponse)
def clear_cart(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Clear cart.
    """
    cart = crud.cart.get_by_user(db=db, user_id=current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart = crud.cart.clear_cart(db=db, cart=cart)
    return cart 