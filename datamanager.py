import dotenv
import database
from sqlmodel import Session
from pydantic import BaseModel
from openai import OpenAI
from models import User, UserInfo, UserPlan, Plan
from typing import Optional, List
from roles import FITNESS_ROLE, NUTRITION_ROLE


class Exercise(BaseModel):
    name: str
    description: str
    sets: Optional[int]
    repetitions: Optional[int]
    duration: float

class TrainingsDay(BaseModel):
    day: str
    exercises: List[Exercise]

class TrainingPlan(BaseModel):
    days: List[TrainingsDay]

class Meal(BaseModel):
    name: str
    ingredients: List[str]
    calories: int
    protein: int
    fats: int
    carbohydrates: int
    instructions: str

class Day(BaseModel):
    day: str
    meals: List[Meal]

class NutritionPlan(BaseModel):
    days: List[Day]

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
        user = self.get_user(user_id, db)
        if not user:
            return Result(success=False, message=f"User {user_id} not found", error="Not Found")

        result = self.update_database(user, db, delete=True)
        if result.success:
            return Result(success=True, message=f"User {user_id} deleted successfully")
    
    def create_user_plan(self, user_id: int, db: Session, plan: Plan, runtime: int | None = 7):
        user = self.get_user(user_id, db)
        if not user:
            return Result(success=False, message=f"User {user_id} not found", error="Not Found")
        
        created_plan = self.make_request(user, plan, runtime)
        if created_plan:
            user_plan = UserPlan(user_id=user_id, plan=plan, details=created_plan.model_dump(), runtime=runtime)
            result = self.update_database(user_plan, db)
            if result.success:
                return Result(success=True, message=f"User plan for User {user_id} successfully created")

    def get_user_plan(self, user_id: int, db: Session):
        user = self.get_user(user_id, db)
        if not user:
            return Result(success=False, message=f"User {user_id} not found", error="Not Found")
        
        user_plan = db.query(User)

    def update_database(self, item: User | UserInfo | UserPlan, db: Session, delete=False):
        if delete:
            db.delete(item) 
        else:
            db.add(item)
        db.commit()
        return Result(success=True, message="Database updated successfully")
    
    def make_request(self, user: User, plan: Plan, runtime: int):
        if plan.value == "TRAINING":
            role = FITNESS_ROLE
            format = TrainingPlan
            plan_type = "Training Plan"
        else:
            role = NUTRITION_ROLE
            format = NutritionPlan
            plan_type = "Nutrition Plan"

        completion = self._client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
        {"role": "developer", "content": role},
        {"role": "user", "content": f"Please create a {plan_type} for a person with the following information: {user.user_info} and for the timespan of {runtime}."},
        ],
        max_completion_tokens=1536,
        temperature=0.7,
        response_format=format)

        plan = completion.choices[0].message.parsed
        return plan

    # TODO: make a PDF document for the PLan
    # TODO: get and activate/deactivate function
    # TODO: update user Error resolve
    # TODO: fieldvalidator error find the problem
    # TODO: a function that calculates the price of each plan (printing it on the PDF)

