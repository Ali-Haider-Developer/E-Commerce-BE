from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    products,
    categories,
    orders,
    cart,
    wishlist,
    users,
    settings,
    search,
    upload
)

api_router = APIRouter()

# Auth endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Product endpoints
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(products.router, prefix="/admin/products", tags=["admin-products"])

# Category endpoints
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(categories.router, prefix="/admin/categories", tags=["admin-categories"])

# Order endpoints
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(orders.router, prefix="/admin/orders", tags=["admin-orders"])

# Cart endpoints
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])

# Wishlist endpoints
api_router.include_router(wishlist.router, prefix="/wishlist", tags=["wishlist"])

# User endpoints
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(users.router, prefix="/admin/users", tags=["admin-users"])

# Settings endpoints
api_router.include_router(settings.router, prefix="/admin/settings", tags=["admin-settings"])

# Search endpoints
api_router.include_router(search.router, prefix="/search", tags=["search"])

# File upload endpoints
api_router.include_router(upload.router, prefix="/admin/upload", tags=["admin-upload"])
