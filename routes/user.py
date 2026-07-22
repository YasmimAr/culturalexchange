from database.database import get_session
from services.auth import get_password_hash
from models.user import User, UserCreate, UserPublic

from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter()

@router.post("/user/", response_model=UserPublic)

def create_user(*, user: UserCreate, session: Session = Depends(get_session)):
    hashed = get_password_hash(user.password)

    db_user = User(
    name=user.name,
    email=user.email,
    role=user.role,
    dateOfBirth=user.dateOfBirth,
    country=user.country,
    lions=user.lions,
    language=user.language,
    passwordHash=hashed,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user