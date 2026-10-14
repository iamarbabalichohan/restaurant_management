from sqlalchemy import String, ForeignKey, Integer, Float, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class OrderItem(Base):
    __tablename__="order_item"
    
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"), primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.item_id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(
        Integer, 
        CheckConstraint("quantity >= 1", name="check_order_item_quantity_min"), 
        nullable=False, 
        server_default="1"
    )

    
    item: Mapped["Item"] = relationship(back_populates="order_items")
    order: Mapped["Order"] = relationship(back_populates="order_items")