from pydantic import BaseModel

class BaseUser(BaseModel):
    username: str
    email: str
    password: str

class CreateUser(BaseUser):
    ...