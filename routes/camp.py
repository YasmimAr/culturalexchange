from database.database import get_session
from models.camp import Camp, CampCreate, CampPublic, CampUpdate

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

router = APIRouter()

def get_camp_or_404(session: Session, camp_id: int) -> Camp:
    camp = session.get(Camp, camp_id)
    if not camp:
        raise HTTPException(status_code=404, detail="Camp not found")
    return camp

@router.post("/camp/", response_model=CampPublic)
def create_camp(*, camp: CampCreate, session: Session = Depends(get_session)):
    db_camp = Camp.model_validate(camp)
    session.add(db_camp)
    session.commit()
    session.refresh(db_camp)
    return db_camp

@router.get("/camp/", response_model=list[CampPublic])
def read_camps(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    camps = session.exec(select(Camp).offset(offset).limit(limit)).all()
    return camps

@router.get("/camp/{camp_id}", response_model=CampPublic)
def read_camp(*, session: Session = Depends(get_session), camp_id: int):
    return get_camp_or_404(session, camp_id)

@router.patch("/camp/{camp_id}", response_model=CampPublic)
def update_camp(*, session: Session = Depends(get_session), camp_id: int, camp: CampUpdate):
    db_camp = get_camp_or_404(session, camp_id)
    camp_data = camp.model_dump(exclude_unset=True)
    db_camp.sqlmodel_update(camp_data)
    session.add(db_camp)
    session.commit()
    session.refresh(db_camp)
    return db_camp

@router.delete("/camp/{camp_id}")
def delete_camp(*, session: Session = Depends(get_session), camp_id: int):
    db_camp = get_camp_or_404(session, camp_id)
    session.delete(db_camp)
    session.commit()
    return {"ok": True}