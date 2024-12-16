from sqlmodel import SQLModel, Field, Relationship, ARRAY, Column, Enum as PgEnum
from pydantic import EmailStr, BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class Sex(Enum):
    FEMALE = "female"
    MALE = "male"


class TrainingPreferences(Enum):
    GYM = "gym"
    CALISTHENICS = "calisthenics"
    HOME = "home"
    BODYWEIGHT = "bodyweight"
    CARDIO = "cardio"


class Goals(Enum):
    WEIGHTLOSS = "weight loss"
    WEIGHTGAIN = "weight gain"
    MUSCLEGAIN = "muscle gain"
    CARDIO = "cardio"
    STRETCH = "stretch"


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    user_info: Optional["UserInfo"] = None


class UserInfo(SQLModel, table=True):
    user_id: int = Field(primary_key=True, foreign_key="user.id")
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

    user_info: Optional[UserInfo] = Relationship(back_populates="user")