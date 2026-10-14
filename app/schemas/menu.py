from pydantic import BaseModel

class BaseMenu(BaseModel):
    name: str
    restaurant_id: int
    
class CreateMenu(BaseMenu):
    ...