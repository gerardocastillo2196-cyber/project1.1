from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel

# Importaciones internas (Si alguna falla, te avisaré en el Paso 2)
from app.db.database import get_db
from app.db.models import User
from app.core.security import verify_password, create_access_token

router = APIRouter()

# Esquema de datos para el Login
class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/token") 
def login_for_access_token(
    form_data: UserLogin, 
    db: Annotated[Session, Depends(get_db)]
):
    # 1. Buscar usuario en BD
    user = db.query(User).filter(User.username == form_data.username).first()

    # 2. Validar contraseña
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    
    # 3. Crear Token (2 horas)
    access_token = create_access_token(subject=user.id)

    return {"access_token": access_token, "token_type": "bearer"}