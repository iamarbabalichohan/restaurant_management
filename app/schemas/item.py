from pydantic import BaseModel

class BaseItem(BaseModel):
    name: str
    quantity: int
    price: float
    menu_id: int
    
class CreateItem(BaseItem):
    ...