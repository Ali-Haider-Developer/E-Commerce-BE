from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import Product, ProductVariant
from app.schemas.product import ProductCreate, ProductUpdate, ProductVariantCreate, ProductVariantUpdate

class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc"
    ) -> List[Product]:
        query = db.query(self.model)
        
        if category_id:
            query = query.filter(self.model.category_id == category_id)
        
        if search:
            query = query.filter(
                (self.model.name.ilike(f"%{search}%")) |
                (self.model.description.ilike(f"%{search}%"))
            )
        
        if min_price is not None:
            query = query.filter(self.model.price >= min_price)
        
        if max_price is not None:
            query = query.filter(self.model.price <= max_price)
        
        if sort_by:
            if sort_order == "desc":
                query = query.order_by(getattr(self.model, sort_by).desc())
            else:
                query = query.order_by(getattr(self.model, sort_by))
        
        return query.offset(skip).limit(limit).all()

    def get_featured(self, db: Session, *, limit: int = 10) -> List[Product]:
        return db.query(self.model).filter(self.model.is_featured == True).limit(limit).all()

    def get_new_arrivals(self, db: Session, *, limit: int = 10) -> List[Product]:
        return db.query(self.model).filter(self.model.is_new_arrival == True).limit(limit).all()

class CRUDProductVariant(CRUDBase[ProductVariant, ProductVariantCreate, ProductVariantUpdate]):
    def get_by_product(self, db: Session, *, product_id: int) -> List[ProductVariant]:
        return db.query(self.model).filter(self.model.product_id == product_id).all()

    def get_by_sku(self, db: Session, *, sku: str) -> Optional[ProductVariant]:
        return db.query(self.model).filter(self.model.sku == sku).first()

product = CRUDProduct(Product)
product_variant = CRUDProductVariant(ProductVariant)