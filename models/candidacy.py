from datetime import date
from enum import StrEnum

from sqlmodel import Field, SQLModel

class DefineStatus(StrEnum):
    approved = "approved"
    pending = "pending"
    rejected = "rejected"
    canceled = "canceled"

class Candidacy(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    userId: int = Field(foreign_key="user.id")
    campId: int = Field(foreign_key="camp.id")
    status: DefineStatus = Field(default=DefineStatus.pending)
    message: str
    createdAt: date = Field(default_factory=date.today)
    priority: int