import database
from typing import Optional
from fastapi import FastAPI, HTTPException, Response
from sqlmodel import select
from database import db_depend
from models import User, UserResponse, UserInfo

app = FastAPI()


@app.get("/user/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: db_depend):
    user = db.get(User, user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found!")


@app.post("/user")
async def create_user(user: User, db: db_depend):
    db.add(user)
    db.commit()
    db.refresh(user)
    return Response(status_code=200, content={"detail": f"User {user.id} created successfully", "data": user.model_dump()})


@app.put("/user/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: User, user_info_data: Optional[UserInfo], db: db_depend):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    new_data = user_data.model_dump(exclude_unset=True)
    for key, value in new_data.items():
        setattr(user, key, value)

    if user_info_data:
        statement = select(UserInfo).where(UserInfo.user_id == user_id)
        user_info = db.exec(statement).first()

        if user_info:
            new_info_data = user_info_data.model_dump(exclude_unset=True)
            for key, value in new_info_data.items():
                setattr(user_info, key, value)
            db.add(user_info)
        else:
            new_user_info = UserInfo(user_id=user_id, **user_info_data.model_dump())
            db.add(new_user_info)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return Response(status_code=200, content={"detail": f"User {user_id} successfully updated", "data": user.model_dump()})


@app.delete("/user/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, db: db_depend):
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
        return Response(status_code=200, content={"detail": f"User {user_id} deleted successfully", "data": user.model_dump()})
    raise HTTPException(status_code=404, detail="User not found!")
