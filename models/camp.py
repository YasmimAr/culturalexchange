from datetime import date
from decimal import Decimal
from enum import StrEnum

from sqlmodel import Field, SQLModel

class DefineStatus(StrEnum):
    new = "new"
    notListed = "notListed"
    early = "early"
    canceled = "canceled"

class Camp(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
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
    createdAt: date = Field(default_factory=date.today)
    hostId: int = Field(foreign_key="user.id")