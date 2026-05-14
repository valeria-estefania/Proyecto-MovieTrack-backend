from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.db import engine, Base
from app.routers import users, auth, content, favorites, status, reviews, actor, admin

import app.models

app = FastAPI(title="MovieTrack API")

# CORS - permite que Flutter se comunique con el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción reemplazar con la URL real del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(content.router)
app.include_router(favorites.router)
app.include_router(status.router)
app.include_router(reviews.router)
app.include_router(actor.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "MovieTrack API funcionando"}