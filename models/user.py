from datetime import date
from enum import StrEnum

from sqlmodel import Field, SQLModel

class DefineRole(StrEnum):
    host = "host"
    assistant = "assistant"
    participant = "participant"

class UserBase(SQLModel):
    name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    role: DefineRole = Field(index=True)
    dateOfBirth: date
    country: str
    lions: str
    language: str

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    passwordHash: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class UserPublic(UserBase):
    id: int