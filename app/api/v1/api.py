from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    users,
    products,
    categories,
    orders,
    cart,
    wishlist,
    settings,
)

api_router = APIRouter()

# Auth endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# User endpoints
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Product endpoints
api_router.include_router(products.router, prefix="/products", tags=["products"])

# Category endpoints
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])

# Order endpoints
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])

# Cart endpoints
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])

# Wishlist endpoints
api_router.include_router(wishlist.router, prefix="/wishlist", tags=["wishlist"])

# Settings endpoints
api_router.include_router(settings.router, prefix="/settings", tags=["settings"]) 