from database.database import get_session
from models.candidacy import Candidacy, CandidacyCreate, CandidacyPublic

from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter()

@router.post("/candidacy/", response_model=CandidacyPublic)

def create_candidacy(*, candidacy: CandidacyCreate, session: Session = Depends(get_session)):
    db_candidacy = Candidacy.model_validate(candidacy)
    session.add(db_candidacy)
    session.commit()
    session.refresh(db_candidacy)
    return db_candidacy