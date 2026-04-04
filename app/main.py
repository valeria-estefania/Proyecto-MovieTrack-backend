from fastapi import FastAPI
from db.db import engine, Base
from routers.auth import router as auth_router
import models
from routers.users import router as user_router
from routers.content import router as content_router
from routers.favorites import router as favorites_router
from routers.status import router as status_router
from routers.reviews import router as reviews_router

app = FastAPI(title="MovieTrack API")

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(content_router)
app.include_router(favorites_router)
app.include_router(status_router)
app.include_router(reviews_router)

@app.get("/")
def root():
    return {"message": "MovieTrack API funcionando"}