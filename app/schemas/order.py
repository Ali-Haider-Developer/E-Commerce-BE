from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from app.models.order import OrderStatus, PaymentStatus
from .product import ProductResponse, ProductVariantResponse

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(OrderItemBase):
    quantity: Optional[int] = None
    price: Optional[float] = None

class OrderItemInDBBase(OrderItemBase):
    id: int
    order_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderItem(OrderItemInDBBase):
    pass

class OrderItemResponse(OrderItemInDBBase):
    pass

class OrderBase(BaseModel):
    shipping_address: Dict[str, Any]
    payment_method: str
    status: OrderStatus = OrderStatus.PENDING

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(OrderBase):
    shipping_address: Optional[Dict[str, Any]] = None
    payment_method: Optional[str] = None
    status: Optional[OrderStatus] = None

class OrderInDBBase(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Order(OrderInDBBase):
    items: List[OrderItem] = []

class OrderResponse(OrderInDBBase):
    items: List[OrderItemResponse] = []

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
