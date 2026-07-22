from datetime import date
from enum import StrEnum

from sqlmodel import Field, SQLModel

class DefineRole(StrEnum):
    host = "host"
    assistant = "assistant"
    participant = "participant"

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    passwordHash: str
    email: str = Field(index=True, unique=True)
    role: DefineRole = Field(index=True)
    dateOfBirth: date
    country: str
    lions: str
    language: str