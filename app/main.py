from fastapi import FastAPI

app = FastAPI(title="MovieTrack API")

@app.get("/")
def root():
    return {"message": "MovieTrack API funcionando"}