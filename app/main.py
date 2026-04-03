from fastapi import FastAPI
from app.db.db import engine, Base
from app.routers.auth import router as auth_router
import app.models

app = FastAPI(title="MovieTrack API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "MovieTrack API funcionando"}