from fastapi import FastAPI, HTTPException, status
from api.api_models import UserCreate, DeleteUser, ChangePassword, UsersList, Message
from models.user import User
from models.messages import Message as M
from typing import List

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
    
@app.put("/update_password")
def update_password(data: ChangePassword):

    u = User.load_user_by_username(data.username)

    if u is None:
        return {"error": "users does not exist"}

    try:
        u.set_new_pass(data.old_password, data.password)
        u._update
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e))
    

@app.get("/users_list")
def get_users_list():
    u = User.load_all_users()
    return u


@app.get("/username/{username}", response_model=UsersList)
def get_user_by_username(username):
    u = User.load_user_by_username(username)
    return u


@app.get("/id/{id}", response_model=UsersList)
def get_user_by_id(id):
    u = User.load_user_by_id(id)
    return u

@app.post("/message")
def send_message(data: Message):
    m = M(data.from_id, data.to_id, data.text)
    m.save_to_db()
    return m


@app.get("/messages_list")
def get_message_list():
    m = M.load_all_messages()
    print(f"debug {m}")
    return m
