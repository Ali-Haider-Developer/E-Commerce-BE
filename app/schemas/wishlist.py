from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .product import ProductResponse

class WishlistItemBase(BaseModel):
    product_id: int

class WishlistItemCreate(WishlistItemBase):
    pass

class WishlistItemUpdate(WishlistItemBase):
    pass

class WishlistItemInDBBase(WishlistItemBase):
    id: int
    wishlist_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WishlistItem(WishlistItemInDBBase):
    pass

class WishlistItemResponse(WishlistItemInDBBase):
    pass

class WishlistBase(BaseModel):
    pass

class WishlistCreate(WishlistBase):
    pass

class WishlistUpdate(WishlistBase):
    pass

class WishlistInDBBase(WishlistBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Wishlist(WishlistInDBBase):
    items: List[WishlistItem] = []

class WishlistResponse(WishlistInDBBase):
    items: List[WishlistItemResponse] = [] 

    