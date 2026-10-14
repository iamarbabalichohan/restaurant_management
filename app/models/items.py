from sqlalchemy import String, ForeignKey, Integer, Float, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Item(Base):
    __tablename__="items"
    
    item_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    price: Mapped[float] = mapped_column(
        Float, 
        CheckConstraint("price >= 0.0", name="check_order_item_price_min"), 
        nullable=False, 
        server_default="0.0"
    )
    menu_id: Mapped[int] = mapped_column(ForeignKey("menus.menu_id", ondelete="CASCADE"))
    
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="item")
    menu: Mapped["Menu"] = relationship(back_populates="items")