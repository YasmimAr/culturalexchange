from datetime import date

from sqlmodel import Field, SQLModel

class User:
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    passwordHash: str
    email: str = Field(index=True)
    role: str = Field(index=True)
    dateOfBirth: date
    country: str
    lions: int
    language: str