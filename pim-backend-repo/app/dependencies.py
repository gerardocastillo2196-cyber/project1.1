from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.core.security import decode_access_token

# 1. Definimos de dónde viene el token (Endpoint de login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# 2. Función para obtener el usuario actual desde el Token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Decodificamos el token
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Buscamos el ID del usuario en el payload (lo guardamos como 'sub')
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token sin credenciales")
        
    # Buscamos al usuario en la Base de Datos
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
    return user

# 3. Función para verificar si es ADMIN (El filtro VIP)
def get_current_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de Administrador"
        )
    return user