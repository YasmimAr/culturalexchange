from database.database import get_session
from services.auth import get_password_hash
from models.user import User, UserCreate, UserPublic, UserUpdate

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

router = APIRouter()

def get_user_or_404(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

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

@router.get("/user/", response_model=list[UserPublic])
def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@router.get("/user/{user_id}", response_model=UserPublic)
def read_user(*, session: Session = Depends(get_session), user_id: int):
    return get_user_or_404(session, user_id)

@router.patch("/user/{user_id}", response_model=UserPublic)  
def update_user(*, session: Session = Depends(get_session), user_id: int, user: UserUpdate):
    db_user = get_user_or_404(session, user_id)
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/user/{user_id}")
def delete_user(*, session: Session = Depends(get_session), user_id: int):
    db_user = get_user_or_404(session, user_id)
    session.delete(db_user)
    session.commit()
    return {"ok": True}