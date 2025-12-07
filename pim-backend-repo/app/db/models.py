from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DECIMAL, Text, Table
from sqlalchemy.orm import relationship
from app.db.database import Base

#TABLA DE UNIÓN (MUCHOS A MUCHOS)
# Esta tabla no es una clase porque solo sirve para conectar Catálogos con Productos
catalog_products = Table(
    'catalog_products',
    Base.metadata,
    Column('catalog_id', Integer, ForeignKey('catalogs.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

#1. USUARIOS 
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="seller")
    is_active = Column(Boolean, default=True)

#2. PAÍSES Y CATEGORÍAS (Tablas Maestras)
class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(3), unique=True, index=True) # GT, SV, HN
    name = Column(String(50))

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)

# 3. EL PRODUCTO (Núcleo)
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True)
    default_name = Column(String(150))
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Relaciones: Aquí se conecta el producto con sus partes
    category_obj = relationship("Category") # Para acceder al nombre de la categoría
    localizations = relationship("ProductLocalization", back_populates="product")
    variants = relationship("ProductVariant", back_populates="product")
    images = relationship("ProductImage", back_populates="product")

    #Relación: Para saber en qué catálogos aparece este producto
    catalogs = relationship("Catalog", secondary=catalog_products, back_populates="products")

#4. TROPICALIZACIÓN (Nombres por país)
class ProductLocalization(Base):
    __tablename__ = "product_localizations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    country_id = Column(Integer, ForeignKey("countries.id"))
    localized_name = Column(String(150))

    product = relationship("Product", back_populates="localizations")
    country = relationship("Country")

#5. VARIANTES (Inventario por color)
class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    color = Column(String(50))
    stock_quantity = Column(Integer, default=0)
    price = Column(DECIMAL(10, 2))

    product = relationship("Product", back_populates="variants")

#6. IMÁGENES
class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    image_url = Column(Text)
    is_primary = Column(Boolean, default=False)

    product = relationship("Product", back_populates="images")

#7. CATÁLOGOS (Nuevos)
class Catalog(Base):
    __tablename__ = "catalogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    target_audience = Column(String(50)) # Ej: 'Industrial' o 'Hogar'

    # Relación mágica: Accedemos a los productos de este catálogo directamente
    products = relationship("Product", secondary=catalog_products, back_populates="catalogs")