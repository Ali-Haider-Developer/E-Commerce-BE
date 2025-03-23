from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.crud import product as product_crud
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductVariantCreate,
    ProductVariantUpdate,
    ProductVariantResponse
)
from app.models.user import UserRole, User

router = APIRouter()

# Admin endpoints
@router.get("/", response_model=List[ProductResponse])
def get_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve products.
    """
    products = crud.product.get_multi(
        db, skip=skip, limit=limit, category_id=category_id, search=search
    )
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get product by ID.
    """
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: ProductCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new product.
    """
    product = crud.product.create(db=db, obj_in=product_in)
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    product_in: ProductUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a product.
    """
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = crud.product.update(db=db, db_obj=product, obj_in=product_in)
    return product

@router.delete("/{product_id}")
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a product.
    """
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = crud.product.remove(db=db, id=product_id)
    return {"ok": True}

# Product variants (admin only)
@router.post("/{product_id}/variants", response_model=ProductVariantResponse)
def create_product_variant(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    variant_in: ProductVariantCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new product variant.
    """
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    variant = crud.product_variant.create(db=db, obj_in=variant_in, product_id=product_id)
    return variant

@router.put("/{product_id}/variants/{variant_id}", response_model=ProductVariantResponse)
def update_product_variant(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    variant_id: int,
    variant_in: ProductVariantUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a product variant.
    """
    variant = crud.product_variant.get(db=db, id=variant_id, product_id=product_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Product variant not found")
    variant = crud.product_variant.update(db=db, db_obj=variant, obj_in=variant_in)
    return variant

@router.delete("/{product_id}/variants/{variant_id}")
def delete_product_variant(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    variant_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a product variant.
    """
    variant = crud.product_variant.get(db=db, id=variant_id, product_id=product_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Product variant not found")
    variant = crud.product_variant.remove(db=db, id=variant_id)
    return {"ok": True}

# User endpoints
@router.get("/public", response_model=List[ProductResponse])
def get_public_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
) -> Any:
    """
    List all products (public)
    """
    products = crud.product.get_multi(
        db, skip=skip, limit=limit, category_id=category_id, search=search
    )
    return products

@router.get("/public/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get product by ID (public)
    """
    product = crud.product.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product

@router.get("/public/{product_id}/variants", response_model=List[ProductVariantResponse])
def get_product_variants(
    product_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get product variants (public)
    """
    product = crud.product.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product.variants

# Featured and New Arrivals endpoints
@router.get("/featured", response_model=List[ProductResponse])
def get_featured_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 10,
) -> Any:
    """
    Get featured products
    """
    products = crud.product.get_featured(db=db, skip=skip, limit=limit)
    return products

@router.get("/new-arrivals", response_model=List[ProductResponse])
def get_new_arrivals(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 10,
) -> Any:
    """
    Get new arrivals
    """
    products = crud.product.get_new_arrivals(db=db, skip=skip, limit=limit)
    return products

# Product images (admin only)
@router.post("/admin/{product_id}/images")
async def upload_product_images(
    product_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Upload product images (Admin only)
    """
    product = crud.product.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return await crud.product.upload_product_images(db, product_id, files) 