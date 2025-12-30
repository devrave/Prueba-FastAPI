from fastapi import FastAPI
from app.core.config import settings
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router

app = FastAPI(
    title=settings.APP_NAME,
    description="API REST para gestión de tareas con autenticación JWT"
)

app.include_router(health_router) #Ruta de verificación de estado
app.include_router(auth_router) #Ruta de autenticación
app.include_router(tasks_router) #Ruta de gestión de tareas
