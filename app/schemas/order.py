from enum import Enum
from pydantic import BaseModel

class PaymentMethodEnum(str, Enum):
    CARD = "CARD"
    COD = "COD"
    
class DeliveryAddress(BaseModel):
    latitude: float
    longitude: float
    
class Item(BaseModel):
    item_id: int
    quantity: int

class BaseOrder(BaseModel):
    restaurant_id: int
    delivery_address: DeliveryAddress

class CreateOrder(BaseOrder):
    items: list[Item]
    payment_method: PaymentMethodEnum