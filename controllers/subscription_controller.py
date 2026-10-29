from collections import defaultdict
from collections.abc import Generator

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import SessionLocal
from models.db_models import Coleccion, Lanzamiento, Suscripcion
from models.schemas import (
    ColeccionCreate,
    ColeccionResponse,
    LanzamientoCreate,
    LanzamientoResponse,
    SuscripcionCreate,
)

router = APIRouter(prefix="/api", tags=["Subscriptions"])

MESES_EN_ESPANOL = (
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/colecciones", response_model=ColeccionResponse)
def crear_coleccion(
    coleccion: ColeccionCreate,
    db: Session = Depends(get_db),
) -> Coleccion:
    nueva_coleccion = Coleccion(**coleccion.model_dump())
    db.add(nueva_coleccion)
    db.commit()
    db.refresh(nueva_coleccion)
    return nueva_coleccion


@router.get("/colecciones", response_model=list[ColeccionResponse])
def listar_colecciones(db: Session = Depends(get_db)) -> list[Coleccion]:
    return db.query(Coleccion).order_by(Coleccion.nombre.asc()).all()


@router.post("/lanzamientos", response_model=LanzamientoResponse)
def crear_lanzamiento(
    lanzamiento: LanzamientoCreate,
    db: Session = Depends(get_db),
) -> Lanzamiento:
    nuevo_lanzamiento = Lanzamiento(**lanzamiento.model_dump())
    db.add(nuevo_lanzamiento)
    db.commit()
    db.refresh(nuevo_lanzamiento)
    return nuevo_lanzamiento


@router.post("/suscribir", response_model=None)
def crear_suscripcion(
    suscripcion: SuscripcionCreate,
    db: Session = Depends(get_db),
) -> Suscripcion:
    nueva_suscripcion = Suscripcion(**suscripcion.model_dump())
    db.add(nueva_suscripcion)
    db.commit()
    db.refresh(nueva_suscripcion)
    return nueva_suscripcion


@router.get("/calendario")
def obtener_calendario(
    email: str | None = None,
    db: Session = Depends(get_db),
) -> dict[str, list[dict[str, object]]]:
    lanzamientos = (
        db.query(Lanzamiento)
        .order_by(Lanzamiento.fecha_lanzamiento.asc())
        .all()
    )

    colecciones_suscritas: set[int] = set()
    if email:
        colecciones_suscritas = {
            coleccion_id
            for (coleccion_id,) in db.query(Suscripcion.coleccion_id)
            .filter(Suscripcion.user_email == email)
            .all()
        }

    calendario: defaultdict[str, list[dict[str, object]]] = defaultdict(list)
    for lanzamiento in lanzamientos:
        fecha = lanzamiento.fecha_lanzamiento
        mes_y_ano = f"{MESES_EN_ESPANOL[fecha.month - 1]} {fecha.year}"
        calendario[mes_y_ano].append(
            {
                "id": lanzamiento.id,
                "coleccion_id": lanzamiento.coleccion_id,
                "entrega_numero": lanzamiento.entrega_numero,
                "titulo_entrega": lanzamiento.titulo_entrega,
                "fecha_lanzamiento": fecha,
                "usuario_suscrito": lanzamiento.coleccion_id
                in colecciones_suscritas,
            }
        )

    return dict(calendario)