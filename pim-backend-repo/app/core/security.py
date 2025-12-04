#python code:
"from datetime import datetime, timedelta"
from typing import Any
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings # Importamos la configuración (clave secreta y 120 minutos)