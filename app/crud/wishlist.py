from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.wishlist import Wishlist, WishlistItem
from app.schemas.wishlist import WishlistItemCreate, WishlistItemUpdate
from app.crud.base import CRUDBase

class CRUDWishlist(CRUDBase[Wishlist, WishlistItemCreate, WishlistItemUpdate]):
    def get_by_user(self, db: Session, *, user_id: int) -> Optional[Wishlist]:
        return db.query(Wishlist).filter(Wishlist.user_id == user_id).first()

    def get_or_create(self, db: Session, *, user_id: int) -> Wishlist:
        wishlist = self.get_by_user(db, user_id=user_id)
        if not wishlist:
            wishlist = Wishlist(user_id=user_id)
            db.add(wishlist)
            db.commit()
            db.refresh(wishlist)
        return wishlist

    def add_item(
        self,
        db: Session,
        *,
        wishlist_id: int,
        item_in: WishlistItemCreate
    ) -> WishlistItem:
        # Check if item already exists
        existing_item = db.query(WishlistItem).filter(
            WishlistItem.wishlist_id == wishlist_id,
            WishlistItem.product_id == item_in.product_id,
            WishlistItem.variant_id == item_in.variant_id
        ).first()

        if existing_item:
            return existing_item

        # Create new item if it doesn't exist
        db_item = WishlistItem(**item_in.dict(), wishlist_id=wishlist_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def remove_item(self, db: Session, *, item_id: int) -> bool:
        db_item = db.query(WishlistItem).filter(WishlistItem.id == item_id).first()
        if not db_item:
            return False

        db.delete(db_item)
        db.commit()
        return True

    def clear_wishlist(self, db: Session, *, wishlist_id: int) -> bool:
        db.query(WishlistItem).filter(WishlistItem.wishlist_id == wishlist_id).delete()
        db.commit()
        return True

wishlist = CRUDWishlist(Wishlist)
wishlist_item = CRUDWishlist(WishlistItem) 

