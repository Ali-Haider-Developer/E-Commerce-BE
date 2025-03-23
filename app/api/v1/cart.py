from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartCreate, CartResponse, CartItemCreate

router = APIRouter()

@router.get("/", response_model=CartResponse)
async def get_cart(db: Session = Depends(get_db)):
    # TODO: Implement get cart logic
    pass

@router.post("/items", response_model=CartResponse)
async def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):
    # TODO: Implement add to cart logic
    pass

@router.put("/items/{item_id}", response_model=CartResponse)
async def update_cart_item(item_id: int, item: CartItemCreate, db: Session = Depends(get_db)):
    # TODO: Implement update cart item logic
    pass

@router.delete("/items/{item_id}", response_model=CartResponse)
async def remove_from_cart(item_id: int, db: Session = Depends(get_db)):
    # TODO: Implement remove from cart logic
    pass 