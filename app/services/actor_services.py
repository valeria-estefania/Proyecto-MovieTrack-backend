from sqlalchemy.orm import Session
from models.actor import Actor
from models.cast import Cast
from schemas.cast import CastResponse
from utils.tmdb import obtener_creditos_tmdb

def extraer_actores(creditos: dict) -> list:
    return [
        {
            "tmdb_id": a["id"],
            "name": a["name"],
            "photo_url": f"https://image.tmdb.org/t/p/w185{a['profile_path']}" if a.get("profile_path") else "",
            "character": a["character"]
        }
        for a in creditos.get("cast", [])[:10]
    ]

def get_o_guardar_actores(db: Session, id_content: int, tmdb_id: int) -> list[CastResponse]:
    existentes = db.query(Cast).filter(Cast.id_content == id_content).all()
    if existentes:
        return [CastResponse.model_validate(c) for c in existentes]

    creditos = obtener_creditos_tmdb(tmdb_id)
    actores = extraer_actores(creditos)

    for a in actores:
        actor = db.query(Actor).filter(Actor.tmdb_id == a["tmdb_id"]).first()
        if not actor:
            actor = Actor(tmdb_id=a["tmdb_id"], name=a["name"], photo_url=a["photo_url"])
            db.add(actor)
            db.flush()

        cast = Cast(id_content=id_content, id_actor=actor.id_actor, character=a["character"])
        db.add(cast)

    db.commit()
    nuevo_cast = db.query(Cast).filter(Cast.id_content == id_content).all()
    return [CastResponse.model_validate(c) for c in nuevo_cast]