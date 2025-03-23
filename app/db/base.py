from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str
    
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

# Import all models here for Alembic to detect them
from app.db.base_class import Base
from app.models.user import User
from app.models.product import Product, ProductVariant
from app.models.cart import Cart, CartItem

# Import all models here that are needed by Alembic
__all__ = ["Base", "User", "Product", "ProductVariant", "Cart", "CartItem"]
