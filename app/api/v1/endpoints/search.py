from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.crud import product as product_crud
from app.schemas.product import ProductResponse
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def search_products(
    q: str = Query(..., description="Search query"),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Search products by name, description, or category"""
    return product_crud.search_products(db, q, skip=skip, limit=limit)

@router.get("/suggestions", response_model=List[str])
def get_search_suggestions(
    q: str = Query(..., description="Search query"),
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """Get search suggestions based on query"""
    return product_crud.get_search_suggestions(db, q, limit=limit) 