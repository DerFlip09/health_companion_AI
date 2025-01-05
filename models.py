from sqlmodel import SQLModel, Field, Relationship, ARRAY, JSON, Column, Enum as PgEnum
from pydantic import EmailStr, BaseModel, field_validator
from datetime import datetime, date
from typing import Optional, List, Any, Dict
from enum import Enum

class Sex(Enum):
    FEMALE = "FEMALE"
    MALE = "MALE"


class Plan(Enum):
    TRAINING = "TRAINING"
    MEAL = "MEAL"


class TrainingPreferences(Enum):
    GYM = "GYM"
    CALISTHENICS = "CALISTHENICS"
    HOME = "HOME"
    BODYWEIGHT = "BODYWEIGHT"
    CARDIO = "CARDIO"


class Goals(Enum):
    WEIGHTLOSS = "WEIGHTLOSS"
    WEIGHTGAIN = "WEIGHTGAIN"
    MUSCLEGAIN = "MUSCLEGAIN"
    CARDIO = "CARDIO"
    STRETCH = "STRETCH"


class UserResponse(SQLModel):
    id: int
    username: str
    email: EmailStr
    user_info: Optional["UserInfo"] = None


class UserInfo(SQLModel, table=True):
    user_id: int = Field(primary_key=True, foreign_key="users.id", index=True)
    age: int = Field(ge=14, le=100)
    sex: Sex = Field(sa_column=Column(PgEnum(Sex)))
    height: int = Field(ge=100, le=250)
    weight: int = Field(gt=0)
    trainings_preferences: List[TrainingPreferences] = Field(sa_column=Column(ARRAY(PgEnum(TrainingPreferences))))
    goals: List[Goals] = Field(sa_column=Column(ARRAY(PgEnum(Goals))))

    user: "User" = Relationship(back_populates="user_info")
    

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field(max_length=50)
    email: EmailStr = Field(index=True, unique=True)
    password: str = Field(min_length=8, max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)

    user_info: Optional["UserInfo"] = Relationship(back_populates="user", cascade_delete="all, delete_orphan")
    user_plan: Optional["UserPlan"] = Relationship(back_populates="user", cascade_delete="all, delete_orphan")


class UserPlan(SQLModel, table=True):
    user_id: int = Field(primary_key=True, foreign_key="users.id", index=True)
    plan: Plan = Field(sa_column=Column(PgEnum(Plan)))
    details: Dict[str, Any] = Field(sa_column=Column(JSON)) 
    created_at: date = Field(default_factory=date.today)
    runtime: int = Field()
    active: bool = Field(default=False)

    @field_validator("runtime")
    def validate_runtime(cls, value):
        if value not in [7, 14, 21, 28]:
            raise ValueError("Invalid runtime. Choose from 7, 14, 21, or 28 days.")
        return value

    user: "User" = Relationship(back_populates="user_plan")
