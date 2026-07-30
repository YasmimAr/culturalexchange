from models.user import User
from models.camp import Camp
from models.candidacy import Candidacy

import os
from sqlmodel import Session
from sqlmodel import SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
engine = create_engine(DATABASE_URL, echo=not bool(os.getenv("DATABASE_URL")))

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

if __name__ == "__main__":
    create_db_and_tables()