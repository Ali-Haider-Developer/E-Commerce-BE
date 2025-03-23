from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.wishlist import Wishlist, WishlistItem
from app.schemas.wishlist import WishlistCreate, WishlistResponse, WishlistItemCreate

router = APIRouter()

@router.get("/", response_model=WishlistResponse)
async def get_wishlist(db: Session = Depends(get_db)):
    # TODO: Implement get wishlist logic
    pass

@router.post("/items", response_model=WishlistResponse)
async def add_to_wishlist(item: WishlistItemCreate, db: Session = Depends(get_db)):
    # TODO: Implement add to wishlist logic
    pass

@router.delete("/items/{item_id}", response_model=WishlistResponse)
async def remove_from_wishlist(item_id: int, db: Session = Depends(get_db)):
    # TODO: Implement remove from wishlist logic
    pass 