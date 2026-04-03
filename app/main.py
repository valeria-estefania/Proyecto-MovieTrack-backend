from fastapi import FastAPI
from app.db.db import engine, Base
from app.routers import users, auth
from app.routers import users, auth, content
import app.models

app = FastAPI(title="MovieTrack API")

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "MovieTrack API funcionando"}

