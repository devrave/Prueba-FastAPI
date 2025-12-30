from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.jwt import crear_token_acceso
from app.services.user_service import UserService
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=TokenResponse, status_code=200)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    user = UserService.authenticate_user(db, datos.email, datos.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    token = crear_token_acceso(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
