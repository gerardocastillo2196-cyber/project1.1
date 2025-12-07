from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm 

from app.db.database import get_db
from app.db.models import User
from app.core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/token")
def login_for_access_token(
    #formulario que FastAPI entiende automáticamente
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    # Validacion usuario
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Creacion el token
    access_token = create_access_token(subject=user.id)

    return {"access_token": access_token, "token_type": "bearer"}