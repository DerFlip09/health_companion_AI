import dotenv
import database
from database import db_depend
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
        self._client = OpenAI(api_key=self.api_key)
        self.db = db_depend
    
    def get_user(self, user_id: int):
        user = self.db.get_user(user_id)
        return user if user else None
    
    def update_user(self, user_id: int, user_data: dict | None, user_info_data: dict | None):
        user = self.get_user(user_id)
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
        
        result = self.update_database(user)
        if result.success:
            return Result(success=True, message=f"User {user_id} updated successfully")
    

    def update_database(self, user: User):
        self.db.add(user)
        self.db.commit()
        return Result(success=True, message="Database updated successfully")
        


