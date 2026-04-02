from fastapi import FastAPI
from app.db.db import engine, Base
import app.models

app = FastAPI(title="MovieTrack API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "MovieTrack API funcionando"}