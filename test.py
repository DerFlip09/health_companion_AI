from fastapi import FastAPI, HTTPException, Response

app = FastAPI()

users = [{"id": 1, "name": "peter"},{"id": 2, "name": "anna"}]


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    for user in users:
        if user_id == user["id"]:
            del user
            return Response(status_code=200)
    raise HTTPException(status_code=404, detail="User not found!")
