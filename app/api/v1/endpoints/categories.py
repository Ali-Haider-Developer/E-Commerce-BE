from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.models.user import UserRole

router = APIRouter()

@router.get("/", response_model=List[schemas.CategoryResponse])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Retrieve categories.
    """
    categories = crud.category.get_multi(db, skip=skip, limit=limit)
    return categories

@router.post("/", response_model=schemas.CategoryResponse)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.CategoryCreate,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
):
    """
    Create new category.
    """
    category = crud.category.create(db=db, obj_in=category_in)
    return category

@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    category_in: schemas.CategoryUpdate,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
):
    """
    Update a category.
    """
    category = crud.category.get(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.category.update(db=db, db_obj=category, obj_in=category_in)
    return category

@router.delete("/{category_id}")
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
):
    """
    Delete a category.
    """
    category = crud.category.get(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.category.remove(db=db, id=category_id)
    return {"ok": True}

# User endpoints
@router.get("/public", response_model=List[schemas.CategoryResponse])
def get_public_categories(
    db: Session = Depends(deps.get_db),
) -> List[schemas.CategoryResponse]:
    """
    List all categories (public)
    """
    categories = crud.category.get_multi(db)
    return categories 