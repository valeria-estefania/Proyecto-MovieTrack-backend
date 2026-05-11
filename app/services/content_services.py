from utils.tmdb import obtener_recomendaciones_tmdb
from models.content import Content
from datetime import datetime
from sqlalchemy.orm import Session

def obtener_recomendaciones(db: Session, tmdb_id: int, type: str = "movie") -> list:
    resultados = obtener_recomendaciones_tmdb(tmdb_id, type)
    
    guardados = []
    for item in resultados[:10]:
        # Si ya existe en tu BD, úsala directamente
        existente = db.query(Content).filter(Content.tmdb_id == item["id"]).first()
        if existente:
            guardados.append(existente)
            continue

        # Si no existe, la guardamos igual que en search
        title   = item.get("title") or item.get("name", "")
        release = item.get("release_date") or item.get("first_air_date", "1900-01-01")

        nuevo = Content(
            tmdb_id    = item["id"],
            title      = title,
            description= item.get("overview", ""),
            type       = type,
            release_date = datetime.strptime(release[:10], "%Y-%m-%d").date() if release else None,
            poster_url = f"https://image.tmdb.org/t/p/w500{item.get('poster_path', '')}",
            rating     = item.get("vote_average", 0.0),
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        guardados.append(nuevo)

    return guardados