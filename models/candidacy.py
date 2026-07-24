from datetime import date
from enum import StrEnum

from sqlmodel import Field, SQLModel

class DefineStatus(StrEnum):
    approved = "approved"
    pending = "pending"
    rejected = "rejected"
    canceled = "canceled"

class CandidacyBase(SQLModel):
    campId: int = Field(foreign_key="camp.id")
    message: str
    priority: int

class Candidacy(CandidacyBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    createdAt: date = Field(default_factory=date.today)
    status: DefineStatus = Field(default=DefineStatus.pending)
    userId: int = Field(foreign_key="user.id")

class CandidacyCreate(CandidacyBase):
    pass

class CandidacyUpdate(SQLModel):
    campId: int | None = None
    message: str | None = None
    priority: int | None = None
    status: DefineStatus | None = None

class CandidacyPublic(CandidacyBase):
    id: int
    status: DefineStatus
    userId: int