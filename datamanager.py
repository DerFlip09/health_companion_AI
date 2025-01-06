import dotenv
import database
from sqlmodel import Session
from openai import OpenAI
from models import User
from typing import Optional


class Result():

    def __init__(self, success: bool, message: str, error: Optional[str] = None):
        self.success = success
        self.message = message
        self.error = error


class Datamanager():
    
    def __init__(self):
        self._api_key = dotenv.get_key(".env", "API_KEY")
        self._client = OpenAI(api_key=self._api_key)
    
    def get_user(self, user_id: int, db: Session):
        user = db.get(User, user_id)
        return user if user else None
    
    def create_user(self, user: User, db: Session):
        result = self.update_database(user, db)
        if result.success:
            return Result(success=True, message="User created successfully")
        
    def add_user_info(self, user_id: int, user_info: dict, db: Session):
        user = self.get_user(user_id, db)
        if not user:
            return Result(success=False, message=f"User {user_id} not found", error="Not Found")
        
        user.user_info = user_info
        result = self.update_database(user, db)
        if result.success:
            return Result(success=True, message=f"User information for User {user_id} successfully added")

    def update_user(self, user_id: int, db: Session, user_data: dict | None = None, user_info_data: dict | None = None):
        user = self.get_user(user_id, db)
        if not user:
            return Result(success=False, message=f"User {user_id} not found", error="Not Found")
        
        updates = {
            user: user_data,
            user.user_info: user_info_data
        }

        for target, data in updates.items():
            if data:
                for key, value in data.items():
                    setattr(target, key, value)
        
        result = self.update_database(user, db)
        if result.success:
            return Result(success=True, message=f"User {user_id} updated successfully")
    
    def delete_user(self, user_id: int, db: Session):
        user = self.get_user(user_i, db)
        if not user:
            return Result(success=False, message=f"User {user_id} not found", error="Not Found")

        result = self.update_database(user, db, delete=True)
        if result.success:
            return Result(success=True, message=f"User {user_id} deleted successfully")

    def update_database(self, user: User, db: Session, delete=False):
        if delete:
            db.delete(user)
        else:
            db.add(user)
        db.commit()
        return Result(success=True, message="Database updated successfully")
        


