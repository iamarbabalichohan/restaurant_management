from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Customer(Base):
    __tablename__ = "customers"
    
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, index=True)
    
    orders: Mapped[list["Order"]] = relationship()
    