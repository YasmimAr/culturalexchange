from database.database import get_session
from models.camp import Camp, CampCreate, CampPublic

from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter()

@router.post("/camp/", response_model=CampPublic)

def create_camp(*, camp: CampCreate, session: Session = Depends(get_session)):
    db_camp = Camp.model_validate(camp)
    session.add(db_camp)
    session.commit()
    session.refresh(db_camp)
    return db_camp