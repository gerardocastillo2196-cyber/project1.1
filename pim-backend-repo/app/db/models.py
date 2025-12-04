from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

# Modelo de Usuario (Login)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="seller")
    is_active = Column(Boolean, default=True)

# Aquí agregaremos los productos en la Fase 4