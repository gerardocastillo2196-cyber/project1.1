from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from pydantic import BaseModel
from fastapi import File, UploadFile # recibir archivos
from app.db.models import ProductImage 
from app.db.database import get_db
from app.db.models import Product, Country, Category, User
# Importamos nuestras nuevas dependencias de seguridad
from app.dependencies import get_current_user, get_current_admin

router = APIRouter()

# --- ESQUEMAS (Pydantic) ---
class ProductCreate(BaseModel):
    sku: str
    default_name: str
    description: Optional[str] = None
    category_id: int

class VariantOut(BaseModel):
    color: str
    stock_quantity: int
    price: float

class ProductOut(BaseModel):
    id: int
    sku: str
    name: str 
    description: Optional[str] = None
    category: str
    variants: List[VariantOut] = []

    class Config:
        from_attributes = True

# --- ENDPOINT 1 (LECTURA): Listar Productos (Cualquier usuario logueado) ---
@router.get("/", response_model=List[ProductOut])
def get_products(
    country_code: str = Query("GT", min_length=2, max_length=2),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # <--- Ahora validamos al usuario real
):
    country = db.query(Country).filter(Country.code == country_code.upper()).first()
    if not country:
        raise HTTPException(status_code=404, detail="País no soportado")

    products_db = db.query(Product).options(
        joinedload(Product.variants),
        joinedload(Product.category_obj),
        joinedload(Product.localizations)
    ).all()

    results = []
    for p in products_db:
        # Lógica de Tropicalización
        final_name = p.default_name
        for loc in p.localizations:
            if loc.country_id == country.id:
                final_name = loc.localized_name
                break
        
        results.append({
            "id": p.id,
            "sku": p.sku,
            "name": final_name,
            "description": p.description,
            "category": p.category_obj.name if p.category_obj else "Sin categoría",
            "variants": p.variants
        })

    return results

#ENDPOINT 2 (ESCRITURA): Crear Producto (SOLO ADMIN)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin) # <--- ¡Solo pasa si es Admin!
):
    # 1. Verificar si el SKU ya existe
    if db.query(Product).filter(Product.sku == product_data.sku).first():
        raise HTTPException(status_code=400, detail="El SKU ya existe")

    # 2. Crear el producto
    new_product = Product(
        sku=product_data.sku,
        default_name=product_data.default_name,
        description=product_data.description,
        category_id=product_data.category_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Producto creado exitosamente", "id": new_product.id, "sku": new_product.sku}

    #ENDPOINT 3: SUBIR IMAGEN (SOLO ADMIN)
@router.post("/{product_id}/images", status_code=status.HTTP_201_CREATED)
def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin) # Solo Admin puede subir fotos
):
    # 1. Verificar que el producto existe
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # 2. Validar que sea una imagen (Opcional pero recomendado)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    # 3. Generar un nombre único para el archivo (para no sobrescribir)
    # Ejemplo: "a1b2c3d4.jpg"
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    # Ruta donde se guardará físicamente
    file_location = f"app/static/images/{unique_filename}"
    
    # 4. Guardar el archivo en el disco
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 5. Guardar la referencia en la Base de Datos
    # La URL que guardamos es la ruta web, no la del disco (sin "app/")
    web_url = f"/static/images/{unique_filename}"
    
    new_image = ProductImage(
        product_id=product.id,
        image_url=web_url,
        is_primary=False # Por defecto no es la principal
    )
    
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return {"filename": unique_filename, "url": web_url}