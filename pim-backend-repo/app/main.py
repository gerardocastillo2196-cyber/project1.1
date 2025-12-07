from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import auth, products # Importamos ambos routers
from app.core.config import settings


app = FastAPI(
    title="PIM Central America API",
    version="1.0.0"
)

# Configuración de CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#incluir las rutas 
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Productos"]) 

@app.get("/")
def read_root():
    return {"message": "PIM API V1 Activo"}