import sys
import os

sys.path.append(os.getcwd())


from app.db.database import SessionLocal
from app.core.security import hash_password
from app.db.models import User

def crear_usuario_admin():
    # sesion para hablar con la base de datos
    db = SessionLocal()
    # Datos para el nuevo administrador
    # Nota: el sistema usa 'username' para el login, no el email
    nuevo_username = "admin"
    nuevo_email = "admin@ejemplo.com"
    password_texto = "admin123"

    # Verificacion si ya existe alguien con ese usuario o email
    usuario_existente = db.query(User).filter(
        (User.username == nuevo_username) | (User.email == nuevo_email)
    ).first()

    if usuario_existente:
        print(f"Error: El usuario {nuevo_username} o el email {nuevo_email} ya existen.")
        return

    # Crecion del nuevo usuario respetando los campos de tu models.py
    nuevo_usuario = User(
        username=nuevo_username,
        email=nuevo_email,
        hashed_password=hash_password(password_texto),
        role="admin",     # El sistema usa roles como texto
        is_active=True
    )


    try:
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        print("Usuario creado exitosamente.")
        print(f"Username: {nuevo_username}")
        print(f"Password: {password_texto}")
    except Exception as e:
        print(f"Ocurrio un error al guardar: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    crear_usuario_admin()
