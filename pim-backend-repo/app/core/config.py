import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Carga variables desde el archivo .env
load_dotenv()

class Settings(BaseSettings):
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://pim_backend:clave_para_app@localhost/pim_db")
    
    # Seguridad (Tokens)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "TU_CLAVE_SECRETA_SUPER_LARGA_AQUI")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120 # 2 horas

# Instancia que exportamos para usar en otros archivos
settings = Settings()