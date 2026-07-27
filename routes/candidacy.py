from database.database import get_session
from services.auth import get_current_user
from routes.camp import get_camp_or_404
from models.candidacy import Candidacy, CandidacyCreate, CandidacyPublic, CandidacyUpdate, CandidacyStatusUpdate
from models.user import User

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

router = APIRouter()

def get_candidacy_or_404(session: Session, candidacy_id: int) -> Candidacy:
    candidacy = session.get(Candidacy, candidacy_id)
    if not candidacy:
        raise HTTPException(status_code=404, detail="Candidacy not found")
    return candidacy

@router.post("/candidacy/", response_model=CandidacyPublic)
def create_candidacy(
    *,
    candidacy: CandidacyCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_camp = get_camp_or_404(session, candidacy.campId)
    if db_camp.hostId == current_user.id:
        raise HTTPException(status_code=403, detail="Host cannot apply to their own camp")

    existing = session.exec(
        select(Candidacy).where(
            Candidacy.campId == candidacy.campId,
            Candidacy.userId == current_user.id
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You already applied to this camp")

    user_candidacies = session.exec(
        select(Candidacy).where(Candidacy.userId == current_user.id)
    ).all()
    if len(user_candidacies) >= 3:
        raise HTTPException(status_code=400, detail="Maximum of 3 candidacies reached")

    for c in user_candidacies:
        if c.priority == candidacy.priority:
            raise HTTPException(status_code=400, detail="Priority already used")

    db_candidacy = Candidacy(**candidacy.model_dump(), userId=current_user.id)
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
def update_candidacy(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    candidacy_id: int,
    candidacy: CandidacyUpdate,
):
    db_candidacy = get_candidacy_or_404(session, candidacy_id)
    if db_candidacy.userId != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to update this candidacy")
    candidacy_data = candidacy.model_dump(exclude_unset=True)
    db_candidacy.sqlmodel_update(candidacy_data)
    session.add(db_candidacy)
    session.commit()
    session.refresh(db_candidacy)
    return db_candidacy

@router.patch("/candidacy/{candidacy_id}/status", response_model=CandidacyPublic)
def update_candidacy_status(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    candidacy_id: int,
    candidacy: CandidacyStatusUpdate,
):
    db_candidacy = get_candidacy_or_404(session, candidacy_id)
    db_camp = get_camp_or_404(session, db_candidacy.campId)
    if db_camp.hostId != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to update this status")
    db_candidacy.status = candidacy.status
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