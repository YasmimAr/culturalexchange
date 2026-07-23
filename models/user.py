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

class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    role: DefineRole | None = None
    dateOfBirth: date | None = None
    country: str | None = None
    lions: str | None = None
    language: str | None = None

class UserPublic(UserBase):
    id: int