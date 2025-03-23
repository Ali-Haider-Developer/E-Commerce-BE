from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class ProductVariantBase(BaseModel):
    name: str
    sku: str
    price: float
    stock: int
    attributes: dict

class ProductVariantCreate(ProductVariantBase):
    pass

class ProductVariantUpdate(ProductVariantBase):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    attributes: Optional[dict] = None

class ProductVariantInDBBase(ProductVariantBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductVariant(ProductVariantInDBBase):
    pass

class ProductVariantResponse(ProductVariantBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: str
    category_id: int
    price: float
    stock: int
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None

class ProductInDBBase(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Product(ProductInDBBase):
    variants: List[ProductVariant] = []

class ProductResponse(ProductBase):
    id: int
    variants: List[ProductVariantResponse] = []

    class Config:
        from_attributes = True
