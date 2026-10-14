from pydantic import BaseModel

class BaseRestaurant(BaseModel):
    name: str
    admin_id: int
    
class CreateRestaurant(BaseRestaurant):
    ...