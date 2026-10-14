import enum
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class PaymentMethodEnum(str, enum.Enum):
    CARD = "CARD"
    COD = "COD"
    
class Order(Base):
    __tablename__ = "orders"
    
    order_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.restaurant_id"))
    payment_method: Mapped[PaymentMethodEnum] = mapped_column(Enum(PaymentMethodEnum), nullable=False)
    delivery_address: Mapped["DeliveryAddress"] = relationship(back_populates="order")
    
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    restaurant: Mapped["Restaurant"] = relationship(back_populates="orders")