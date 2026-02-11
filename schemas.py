from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import List

from models import MonthEnum, ExpenseCategoryEnum


class UserBase(BaseModel):
    id: str
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    username: str = Field(min_length=3, max_length=100)


class UserCreate(UserBase):
    password: str = Field(min_length=3, max_length=200)


class TrackerPublic(BaseModel):
    month: MonthEnum
    budget: int
    total_expense: int
    save_expense: int


class UserResponse(UserBase):
    trackers: List[TrackerPublic]


class TrackerCreate(BaseModel):
    month: MonthEnum
    budget: int
    expense_type: List[ExpenseCategoryEnum]


class TrackerResponse(BaseModel):
    id: str
    month: MonthEnum
    budget: int
    expense_type: List[ExpenseCategoryEnum]
    total_expense: int
    total_save: int
    created_at: datetime
