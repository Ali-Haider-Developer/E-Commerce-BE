from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate

def get_orders(db: Session) -> List[Order]:
    return db.query(Order).all()

def get_order(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()

def create_order(db: Session, order: OrderCreate) -> Order:
    db_order = Order(**order.dict(exclude={'items'}))
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items
    for item in order.items:
        db_item = OrderItem(**item.dict(), order_id=db_order.id)
        db.add(db_item)
    
    db.commit()
    return db_order

def update_order(db: Session, order_id: int, order: OrderUpdate) -> Optional[Order]:
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    
    for key, value in order.dict(exclude_unset=True).items():
        if key != 'items':
            setattr(db_order, key, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int) -> bool:
    db_order = get_order(db, order_id)
    if not db_order:
        return False
    
    db.delete(db_order)
    db.commit()
    return True

# Order Items CRUD operations
def add_order_item(db: Session, order_id: int, item: OrderItemCreate) -> Optional[Order]:
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    
    db_item = OrderItem(**item.dict(), order_id=order_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_order)
    return db_order

def remove_order_item(db: Session, order_id: int, item_id: int) -> Optional[Order]:
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    
    db_item = db.query(OrderItem).filter(
        OrderItem.id == item_id,
        OrderItem.order_id == order_id
    ).first()
    
    if not db_item:
        return None
    
    db.delete(db_item)
    db.commit()
    db.refresh(db_order)
    return db_order 