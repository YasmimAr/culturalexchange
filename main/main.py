from fastapi import FastAPI
from routes.camp import router as camp_router
from routes.candidacy import router as candidacy_router
from routes.user import router as user_router
from routes.auth import router as auth_router

app = FastAPI()

app.include_router(camp_router)
app.include_router(candidacy_router)
app.include_router(user_router)
app.include_router(auth_router)