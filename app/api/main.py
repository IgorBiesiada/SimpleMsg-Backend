from fastapi import FastAPI, HTTPException, status, Depends
from .api_models import UserCreate, DeleteUser, ChangePassword, UsersList, Message
from models.user import User
from models.messages import Message as M
from typing import Annotated
from psycopg2.extensions import connection as PostgreConnection
from .auth import get_db, get_current_user, router

app = FastAPI()
app.include_router(router)

db_dependency = Annotated[PostgreConnection, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get('/me', status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="failed")
    return {'User': user}

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
def delete_user(data: DeleteUser, user: user_dependency, db: db_dependency):

    user_id = user.get('id')
    
    u = User.load_user_by_id(user_id)
    
    if u is None:
        return {"error": "user does not exist"}
    
    u._delete(data.username)
    return {"status": "ok", "deleted user" : data.username}
    
@app.put("/update_password")
async def update_password(data: ChangePassword, user: user_dependency, db: db_dependency):

    user_id = user.get('id')
    
    u = User.load_user_by_id(user_id)

    if u is None:
        return {"error": "users does not exist"}

    try:
        u.set_new_pass(data.old_password, data.password)
        u._update()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e))
    

@app.get("/users_list", response_model=UsersList)
async def get_users_list():
    u = User.load_all_users()
    return u


@app.get("/username/{username}", response_model=UsersList)
async def get_user_by_username(username):
    u = User.load_user_by_username(username)
    return u


@app.get("/id/{id}", response_model=UsersList)
async def get_user_by_id(id):
    u = User.load_user_by_id(id)
    return u

@app.post("/message")
async def send_message(data: Message, user: user_dependency, db: db_dependency):
    sender_id = user.get('id')
    
    m = M(sender_id, data.to_id, data.text)
    m.save_to_db()
    
    return {
        "status": "Wysłano",
        "from": user.get('username'),
        "message": data.text
    }


@app.get("/messages_list")
def get_message_list(user: user_dependency, db: db_dependency):
    m = M.load_all_messages()
    print(f"debug {m}")
    return m
