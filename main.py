from database import db_depend
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from models import User, UserResponse, UserInfo, UserPlan, Plan
from datamanager import Datamanager

dataman = Datamanager()
app = FastAPI()


@app.get("/user/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: db_depend):
    user = dataman.get_user(user_id, db)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found!")


@app.post("/user/", response_model=UserResponse)
async def create_user(user: User, db: db_depend):
    result = dataman.create_user(user, db)
    if result.success:
        return JSONResponse(status_code=200, content={"detail": result.message})
    

@app.post("/user/user_info/{user_id}", response_model=UserResponse)
async def add_user_info(user_id: int, user_info_data: UserInfo, db: db_depend):
    new_user_info = UserInfo(user_id=user_id, **user_info_data.model_dump())
    result = dataman.add_user_info(user_id, new_user_info, db)
    if result.success:
        return JSONResponse(status_code=200, content={"detail": result.message})
    if result.error == "Not Found":
        raise HTTPException(status_code=404, detail=result.message)
    

@app.put("/user/update/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, db: db_depend, user_data: Optional[User], user_info_data: Optional[UserInfo]) -> UserResponse:
    if not user_data and not user_info_data:
        raise HTTPException(status_code=400, detail="No valid data provided to update.")

    new_data = user_data.model_dump(exclude_unset=True) if user_data else None
    new_info_data = user_info_data.model_dump(exclude_unset=True) if user_info_data else None

    result = dataman.update_user(user_id, db, new_data, new_info_data)
    if result.success:
        return JSONResponse(status_code=200, content={"detail": result.message})
    if result.error == "Not Found":     
        raise HTTPException(status_code=404, detail=result.message)
    

@app.delete("/user/delete/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, db: db_depend):
    result = dataman.delete_user(user_id, db)
    if result.success:
        return JSONResponse(status_code=200, content={"detail": f"User {user_id} deleted successfully"})
    if result.error == "Not Found":
        raise HTTPException(status_code=404, detail="User not found!")


@app.post("/plan/")
async def create_plan(user_id: int, plan: Plan, runtime: int, db: db_depend):
    result = dataman.create_user_plan(user_id, db, plan, runtime)
    if result.success:
        return JSONResponse(status_code=200, content={"detail": result.message})
    if result.error == "Not Found":     
        raise HTTPException(status_code=404, detail=result.message)


@app.get("/user/{user_id}/plans/")
async def get_active_user_plan(user_id: int, db: db_depend, plan: Plan):
    result = dataman.get_active_user_plan(user_id, db, plan)
    print(result)
    print(type(result))
    if result is None:
        raise HTTPException(status_code=404, detail="User not found or no active plan!")
    else:
        return result