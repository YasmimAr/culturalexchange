from database.database import get_session
from services.auth import get_current_user
from models.camp import Camp, CampCreate, CampPublic, CampUpdate
from models.user import User, DefineRole

from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

router = APIRouter()

def get_camp_or_404(session: Session, camp_id: int) -> Camp:
    camp = session.get(Camp, camp_id)
    if not camp:
        raise HTTPException(status_code=404, detail="Camp not found")
    return camp

@router.post("/camp/", response_model=CampPublic)
def create_camp(
    *,
    camp: CampCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != DefineRole.host:
        raise HTTPException(status_code=403, detail="Only hosts can create camps")

    db_camp = Camp(**camp.model_dump(), hostId=current_user.id)
    session.add(db_camp)
    session.commit()
    session.refresh(db_camp)
    return db_camp

@router.get("/camp/", response_model=list[CampPublic])
def read_camps(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    country: str | None = None,
    language: str | None = None,
    start_after: date | None = None,
    age: int | None = None,
    limit: int = Query(default=100, le=100),
):
    query = select(Camp)
    if country:
        query = query.where(Camp.country == country)
    if language:
        query = query.where(Camp.language == language)
    if start_after:
        query = query.where(Camp.campStartDate >= start_after)
    if age:
        query = query.where(Camp.ageMin <= age, Camp.ageMax >= age)

    camps = session.exec(query.offset(offset).limit(limit)).all()
    return camps

@router.get("/camp/{camp_id}", response_model=CampPublic)
def read_camp(*, session: Session = Depends(get_session), camp_id: int):
    return get_camp_or_404(session, camp_id)

@router.patch("/camp/{camp_id}", response_model=CampPublic)
def update_camp(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    camp_id: int,
    camp: CampUpdate,
):
    db_camp = get_camp_or_404(session, camp_id)
    if db_camp.hostId != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to update this camp")
    camp_data = camp.model_dump(exclude_unset=True)
    db_camp.sqlmodel_update(camp_data)
    session.add(db_camp)
    session.commit()
    session.refresh(db_camp)
    return db_camp

@router.delete("/camp/{camp_id}")
def delete_camp(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    camp_id: int,
):
    db_camp = get_camp_or_404(session, camp_id)
    if db_camp.hostId != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this camp")
    session.delete(db_camp)
    session.commit()
    return {"ok": True}