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
    
    u._delete(user.get('username'))
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
async def get_users_list(user: user_dependency):
    
    
    u = User.load_all_users()
    return u


@app.get("/username/{username}", response_model=UsersList)
async def get_user_by_username(username, user: user_dependency):
    
    u = User.load_user_by_username(username)
    
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Użytkownik o nazwie '{username}' nie został znaleziony")   
    
    return u


@app.get("/id/{id}", response_model=UsersList)
async def get_user_by_id(id, user: user_dependency):
    u = User.load_user_by_id(id)
    
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Użytkownik o if '{id}' nie został znaleziony")   
    
    return u

@app.post("/message")
async def send_message(data: Message, user: user_dependency):
    sender_id = user.get('id')
    receiver = User.load_user_by_id(data.to_id)
    
    if receiver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Odbiorca o ID {data.to_id} nie istnieje!"
        )
    
    if sender_id == receiver.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nie można wysłać wiadomości do samego siebie"
        )
    
    
    m = M(sender_id, data.to_id, data.text)
    
    m.save_to_db()
    
    return {
        "status": "Wysłano",
        "from": user.get('username'),
        "message": data.text
    }


@app.get("/messages_list")
def get_message_list(user: user_dependency):
    
    m = M.load_user_messages(user.get('id'))
    print(f"debug {m}")
    return m
