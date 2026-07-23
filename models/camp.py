from datetime import date
from decimal import Decimal
from enum import StrEnum

from sqlmodel import Field, SQLModel

class DefineStatus(StrEnum):
    new = "new"
    notListed = "notListed"
    early = "early"
    canceled = "canceled"

class CampBase(SQLModel):
    name: str = Field(index=True)
    country: str = Field(index=True)
    province: str
    city: str
    website: str
    lciApprove: date
    applicationDeadLine: date
    campStartDate: date = Field(index=True)
    campEndDate: date = Field(index=True)
    ageMin: int | None = Field(default=None, index=True)
    ageMax: int | None = Field(default=None, index=True)
    participants: int
    fee: Decimal = Field(default=0, max_digits=7, decimal_places=2, index=True)
    currency: str
    description: str
    status: DefineStatus = Field(index=True)
    hostId: int = Field(foreign_key="user.id")

class Camp(CampBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    createdAt: date = Field(default_factory=date.today)

class CampCreate(CampBase):
    pass

class CampUpdate(SQLModel):
    name: str | None = None
    country: str | None = None
    province: str | None = None
    city: str | None = None
    website: str | None = None
    lciApprove: date | None = None
    applicationDeadLine: date | None = None
    campStartDate: date | None = None
    campEndDate: date | None = None
    ageMin: int | None = None
    ageMax: int | None = None
    participants: int | None = None
    fee: Decimal | None = None
    currency: str | None = None
    description: str | None = None
    status: DefineStatus | None = None
    hostId: int | None = None

class CampPublic(CampBase):
    id: int

