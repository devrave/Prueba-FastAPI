from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db

router = APIRouter(prefix="/salud", tags=["Salud"])

@router.get("")
def verificar_estado():
    return {"estado": "ok"}

@router.get("/db")
def verificar_conexion_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"estado": "ok", "database": "conectada"}
