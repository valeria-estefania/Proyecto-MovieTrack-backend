from fastapi import FastAPI
from db.db import engine, Base
from routers import users, auth, content, favorites, status, reviews
import models

app = FastAPI(title="MovieTrack API")

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(content.router)
app.include_router(favorites.router)
app.include_router(status.router)
app.include_router(reviews.router)

@app.get("/")
def root():
    return {"message": "MovieTrack API funcionando"}