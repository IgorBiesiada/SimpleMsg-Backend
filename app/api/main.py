from fastapi import FastAPI
from api.api_models import UserCreate, DeleteUser
from models.user import User

app = FastAPI()

@app.post("/register")
def create_user(data: UserCreate):
    
    if User.load_user_by_username(data.username):
        return {"error": "users already exist"}
    
    new_user = User(username=data.username,
                    password=data.password,
                    first_name=data.first_name,
                    last_name=data.last_name,
                    )

    new_user._insert()
    return {"status": "ok", "dodano": {data.username}}

@app.delete("/delete")
def delete_user(data: DeleteUser):

    u = User.load_user_by_username(data.username)
    
    if u is None:
        return {"error": "user does not exist"}
    
    u._delete(data.username)
    return {"status": "ok", "deleted user" : data.username}
    
    