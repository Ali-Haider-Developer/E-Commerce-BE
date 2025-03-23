from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartItemCreate, CartItemUpdate
from app.crud.base import CRUDBase

class CRUDCart(CRUDBase[Cart, CartItemCreate, CartItemUpdate]):
    def get_by_user(self, db: Session, *, user_id: int) -> Optional[Cart]:
        return db.query(Cart).filter(Cart.user_id == user_id).first()

    def get_or_create(self, db: Session, *, user_id: int) -> Cart:
        cart = self.get_by_user(db, user_id=user_id)
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart

    def add_item(
        self,
        db: Session,
        *,
        cart_id: int,
        item_in: CartItemCreate
    ) -> CartItem:
        # Check if item already exists
        existing_item = db.query(CartItem).filter(
            CartItem.cart_id == cart_id,
            CartItem.product_id == item_in.product_id,
            CartItem.variant_id == item_in.variant_id
        ).first()

        if existing_item:
            # Update quantity if item exists
            existing_item.quantity += item_in.quantity
            db.commit()
            db.refresh(existing_item)
            return existing_item

        # Create new item if it doesn't exist
        db_item = CartItem(**item_in.dict(), cart_id=cart_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def update_item(
        self,
        db: Session,
        *,
        item_id: int,
        item_in: CartItemUpdate
    ) -> Optional[CartItem]:
        db_item = db.query(CartItem).filter(CartItem.id == item_id).first()
        if not db_item:
            return None

        for field, value in item_in.dict(exclude_unset=True).items():
            setattr(db_item, field, value)

        db.commit()
        db.refresh(db_item)
        return db_item

    def remove_item(self, db: Session, *, item_id: int) -> bool:
        db_item = db.query(CartItem).filter(CartItem.id == item_id).first()
        if not db_item:
            return False

        db.delete(db_item)
        db.commit()
        return True

    def clear_cart(self, db: Session, *, cart_id: int) -> bool:
        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
        db.commit()
        return True

cart = CRUDCart(Cart)
cart_item = CRUDCart(CartItem)