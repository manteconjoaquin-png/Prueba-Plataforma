from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from config.database import Base, engine
import models.db_models
from controllers.subscription_controller import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plataforma de Suscripciones y Lanzamientos")
app.include_router(router)
app.mount("/views", StaticFiles(directory="views"), name="views")


@app.get("/")
def mostrar_dashboard() -> FileResponse:
    return FileResponse("views/dashboard.html")