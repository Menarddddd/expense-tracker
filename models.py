import uuid
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Enum as SQLAEnum
from enum import Enum

from database import Base


class MonthEnum(str, Enum):
    JANUARY = "January"
    FEBRUARY = "February"
    MARCH = "March"
    APRIL = "April"
    MAY = "May"
    JUNE = "June"
    JULY = "July"
    AUGUST = "August"
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"


class ExpenseCategoryEnum(str, Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Entertainment"
    OTHERS = "Others"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)

    trackers: Mapped[List[Tracker]] = relationship(
        "Tracker", back_populates="user", cascade="all, delete-orphan"
    )


class Tracker(Base):
    __tablename__ = "trackers"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    month: Mapped[MonthEnum] = mapped_column(SQLAEnum(MonthEnum), nullable=False)
    budget: Mapped[int] = mapped_column(Integer, nullable=False)
    expense_type: Mapped[ExpenseCategoryEnum] = mapped_column(
        SQLAEnum(ExpenseCategoryEnum), nullable=False
    )
    total_expense: Mapped[int] = mapped_column(Integer, nullable=False)
    total_save: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="trackers")
