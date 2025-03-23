from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=schemas.WishlistResponse)
def read_wishlist(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Get user's wishlist.
    """
    wishlist = crud.wishlist.get_or_create(db=db, user_id=current_user.id)
    return wishlist

@router.post("/items", response_model=schemas.WishlistResponse)
def add_to_wishlist(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.WishlistItemCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Add item to wishlist.
    """
    wishlist = crud.wishlist.get_or_create(db=db, user_id=current_user.id)
    wishlist = crud.wishlist.add_item(db=db, wishlist=wishlist, item_in=item_in)
    return wishlist

@router.delete("/items/{item_id}", response_model=schemas.WishlistResponse)
def remove_from_wishlist(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Remove item from wishlist.
    """
    wishlist = crud.wishlist.get_by_user(db=db, user_id=current_user.id)
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    wishlist = crud.wishlist.remove_item(db=db, wishlist=wishlist, item_id=item_id)
    return wishlist

@router.delete("/", response_model=schemas.WishlistResponse)
def clear_wishlist(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Clear wishlist.
    """
    wishlist = crud.wishlist.get_by_user(db=db, user_id=current_user.id)
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    wishlist = crud.wishlist.clear_wishlist(db=db, wishlist=wishlist)
    return wishlist 