from pydantic import BaseModel

class AuthUser(BaseModel):
    username: str
    password: str


class UserCreate(AuthUser):
    first_name: str
    last_name: str
    

class DeleteUser(BaseModel):
    username: str


class ChangePassword(AuthUser):
    old_password: str


class UsersList(BaseModel):
    username: str
    first_name: str
    last_name: str
    

class Message(BaseModel):
    from_id: int
    to_id: int
    text: str