from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Restaurant(Base):
    __tablename__ = "restaurants"
    restaurant_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    admin_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    admin: Mapped["User"] = relationship(back_populates="restaurants")
    
    menus: Mapped[list["Menu"]] = relationship(back_populates="restaurant")
    orders: Mapped[list["Order"]] = relationship(back_populates="restaurant")
