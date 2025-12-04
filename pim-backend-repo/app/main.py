from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth # Importamos la ruta de Login
from app.core.config import settings