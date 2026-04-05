from sqlalchemy.orm import Session
from models.content import Content, content_platform
from models.platform import Platform
from schemas.platform import PlatformResponse
from utils.tmdb import obtener_plataformas_tmdb

def extraer_plataformas(providers: dict, pais: str = "CO") -> list:
    pais_data = providers.get(pais, {})
    return [
        {
            "nombre": p["provider_name"],
            "logo_url": f"https://image.tmdb.org/t/p/w45{p['logo_path']}"
        }
        for p in pais_data.get("flatrate", [])
    ]

def get_o_guardar_plataformas(db: Session, id_content: int, tmdb_id: int) -> list[PlatformResponse]:
    content = db.query(Content).filter(Content.id_content == id_content).first()

    if content.platform:
        return [PlatformResponse.model_validate(p) for p in content.platform]

    #  Tomar el type del propio contenido
    providers = obtener_plataformas_tmdb(tmdb_id, type=content.type)
    plataformas = extraer_plataformas(providers)

    if not plataformas:
        return []

    for p in plataformas:
        plataforma = db.query(Platform).filter(Platform.nombre == p["nombre"]).first()
        if not plataforma:
            plataforma = Platform(nombre=p["nombre"], logo_url=p["logo_url"])
            db.add(plataforma)
            db.flush()

        content.platform.append(plataforma)

    db.commit()
    db.refresh(content)
    return [PlatformResponse.model_validate(p) for p in content.platform]