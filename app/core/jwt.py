from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def crear_token_acceso(data: dict) -> str:
    to_encode = data.copy()
    expiracion = datetime.utcnow() + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expiracion})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
