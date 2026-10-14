from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Menu(Base):
    __tablename__="menus"
    
    menu_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.restaurant_id"))
    
    restaurant: Mapped["Restaurant"] = relationship(back_populates="menus")
    items: Mapped[list["Item"]] = relationship(back_populates="menu")
    