from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import user as user_crud
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.order import OrderResponse
from app.schemas.wishlist import WishlistResponse
from app.db.session import get_db
from app.core.auth import get_current_user
from app.models.user import User as UserModel
from app.api import deps

router = APIRouter()
admin_router = APIRouter()

# Admin endpoints
@admin_router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(deps.get_current_active_superuser),
):
    """
    Retrieve users (admin only)
    """
    users = user_crud.get_multi(db, skip=skip, limit=limit)
    return users

@admin_router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_superuser),
):
    """
    Get user by ID (admin only)
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@admin_router.post("/", response_model=UserResponse)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: UserModel = Depends(deps.get_current_active_superuser),
):
    """
    Create new user (admin only)
    """
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = user_crud.create(db, obj_in=user_in)
    return user

@admin_router.put("/{user_id}", response_model=UserResponse)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: UserModel = Depends(deps.get_current_active_superuser),
):
    """
    Update user (admin only)
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user = user_crud.update(db, db_obj=user, obj_in=user_in)
    return user

@admin_router.delete("/{user_id}")
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: UserModel = Depends(deps.get_current_active_superuser),
):
    """
    Delete user (admin only)
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user_crud.remove(db, id=user_id)
    return {"message": "User deleted successfully"}

@admin_router.get("/statistics")
def get_user_statistics(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_superuser)
):
    """Get user statistics (Admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user_crud.get_statistics(db)

# Customer endpoints
@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: UserModel = Depends(deps.get_current_active_user),
):
    """
    Get current user profile
    """
    return current_user

@router.put("/me", response_model=UserResponse)
def update_current_user_profile(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: UserModel = Depends(deps.get_current_active_user),
):
    """
    Update current user profile
    """
    user = user_crud.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.put("/me/password")
def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """Change current user password"""
    if not user_crud.authenticate(db, email=current_user.email, password=old_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    user_crud.update(db, db_obj=current_user, obj_in={"password": new_password})
    return {"message": "Password updated successfully"}

@router.get("/me/orders", response_model=List[OrderResponse])
def get_current_user_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """Get current user's orders"""
    return user_crud.get_user_orders(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/me/wishlist", response_model=WishlistResponse)
def get_current_user_wishlist(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """Get current user's wishlist"""
    return user_crud.get_user_wishlist(db, user_id=current_user.id) 