from fastapi import FastAPI, HTTPException, Response
from sqlmodel import SQLModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

users = []

class UserIn(SQLModel):
    id: int
    name: str
    password: str


class UserOut(SQLModel):
    id: int
    name: str


@app.post("/user", response_model=UserOut)
def create_user(user: UserIn):
    for u in users:
        if u.name == user.name:
            raise HTTPException(status_code=400, detail="User already exists")
    
    user.id = len(users) + 1
    users.append(user)
    return JSONResponse(status_code=200, content=jsonable_encoder(user))

