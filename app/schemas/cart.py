from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .product import ProductResponse, ProductVariantResponse

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(CartItemBase):
    quantity: Optional[int] = None

class CartItemInDBBase(CartItemBase):
    id: int
    cart_id: int
    price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CartItem(CartItemInDBBase):
    pass

class CartItemResponse(CartItemInDBBase):
    pass

class CartBase(BaseModel):
    pass

class CartCreate(CartBase):
    pass

class CartUpdate(CartBase):
    pass

class CartInDBBase(CartBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Cart(CartInDBBase):
    items: List[CartItem] = []

class CartResponse(CartInDBBase):
    items: List[CartItemResponse] = [] 