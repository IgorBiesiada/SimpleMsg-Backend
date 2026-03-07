from pydantic import BaseModel

class AuthUser(BaseModel):
    username: str
    password: str


class UserCreate(AuthUser):
    first_name: str
    last_name: str
    

class DeleteUser(BaseModel):
    username: str

class UpdateUser():
    pass