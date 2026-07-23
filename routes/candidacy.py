from database.database import get_session
from models.candidacy import Candidacy, CandidacyCreate, CandidacyPublic, CandidacyUpdate

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

router = APIRouter()

def get_candidacy_or_404(session: Session, candidacy_id: int) -> Candidacy:
    candidacy = session.get(Candidacy, candidacy_id)
    if not candidacy:
        raise HTTPException(status_code=404, detail="Candidacy not found")
    return candidacy

@router.post("/candidacy/", response_model=CandidacyPublic)
def create_candidacy(*, candidacy: CandidacyCreate, session: Session = Depends(get_session)):
    db_candidacy = Candidacy.model_validate(candidacy)
    session.add(db_candidacy)
    session.commit()
    session.refresh(db_candidacy)
    return db_candidacy

@router.get("/candidacy/", response_model=list[CandidacyPublic])
def read_candidacies(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    candidacies = session.exec(select(Candidacy).offset(offset).limit(limit)).all()
    return candidacies

@router.get("/candidacy/{candidacy_id}", response_model=CandidacyPublic)
def read_candidacy(*, session: Session = Depends(get_session), candidacy_id: int):
    return get_candidacy_or_404(session, candidacy_id)

@router.patch("/candidacy/{candidacy_id}", response_model=CandidacyPublic)
def update_candidacy(*, session: Session = Depends(get_session), candidacy_id: int, candidacy: CandidacyUpdate):
    db_candidacy = get_candidacy_or_404(session, candidacy_id)
    candidacy_data = candidacy.model_dump(exclude_unset=True)
    db_candidacy.sqlmodel_update(candidacy_data)
    session.add(db_candidacy)
    session.commit()
    session.refresh(db_candidacy)
    return db_candidacy

@router.delete("/candidacy/{candidacy_id}")
def delete_candidacy(*, session: Session = Depends(get_session), candidacy_id: int):
    db_candidacy = get_candidacy_or_404(session, candidacy_id)
    session.delete(db_candidacy)
    session.commit()
    return {"ok": True}
