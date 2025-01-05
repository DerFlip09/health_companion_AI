import database
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from database import db_depend
from models import User, UserResponse, UserInfo, UserPlan

app = FastAPI()


@app.get("/user/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: db_depend):
    user = db.get(User, user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found!")


@app.post("/user/", response_model=UserResponse)
async def create_user(user: User, db: db_depend):
    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse(status_code=200, content={"detail": f"User {user.id} created successfully"})


@app.post("/user/user_info/{user_id}", response_model=UserResponse)
async def post_user_info(user_id: int, user_info_data: UserInfo):
    user = dataman.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    new_user_info = UserInfo(user_id=user_id, **user_info_data.model_dump())
    db.add(new_user_info)
    user.user_info = new_user_info
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse(status_code=200, content={"detail": f"User Information for User {user_id} successfully added"})


@app.put("/user/update/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: Optional[User], user_info_data: Optional[UserInfo], db: db_depend) -> UserResponse:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    if user_data:
        new_data = user_data.model_dump(exclude_unset=True)
        for key, value in new_data.items():
            setattr(user, key, value)

    if user_info_data and user.user_info:
        new_info_data = user_info_data.model_dump(exclude_unset=True)
        for key, value in new_info_data.items():
            setattr(user.user_info, key, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse(status_code=200, content={"detail": f"User {user_id} successfully updated"})


@app.delete("/user/delete/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, db: db_depend):
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
        return JSONResponse(status_code=200, content={"detail": f"User {user_id} deleted successfully"})
    raise HTTPException(status_code=404, detail="User not found!")


@app.post("/plan/")
async def create_plan(plan: UserPlan, db: db_depend):
    return plan
