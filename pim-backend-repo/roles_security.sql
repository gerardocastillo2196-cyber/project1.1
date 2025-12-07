
-- FASE 2: CREACIÓN DE ROLES DE SEGURIDAD

-- 1. CREACIÓN DEL ROL ADMINISTRADOR
-- Este rol puede hacer migraciones y mantenimiento.
CREATE USER pim_admin WITH ENCRYPTED PASSWORD 'tu_clave_admin';
-- Le damos permisos de Superusuario para efectos de desarrollo/migraciones.
ALTER USER pim_admin CREATEDB CREATEROLE;

-- 2. CREACIÓN DEL ROL DE LA APLICACIÓN (EL BACKEND)
-- Este rol lo usará la API de FastAPI. Tendrá permisos muy limitados.
CREATE USER pim_backend WITH ENCRYPTED PASSWORD 'clave_para_app';

-- ASIGNACIÓN DE PRIVILEGIOS AL BACKEND

-- 3. PERMISOS DE CONEXIÓN
-- Permitir que el backend vea todo el esquema (la estructura).
GRANT USAGE ON SCHEMA public TO pim_backend;

-- 4. PERMISOS DE LECTURA (SELECT)
-- La API necesita leer TODAS las tablas (productos, categorías, países, etc.)
GRANT SELECT ON ALL TABLES IN SCHEMA public TO pim_backend;

-- 5. PERMISOS DE ESCRITURA/MODIFICACIÓN (INSERT, UPDATE, DELETE)
-- El backend SOLO puede modificar las tablas de DATO.
-- Las tablas de configuración (Countries, Categories, Catalogs) deben ser solo lectura.

-- Tablas Operacionales (El Backend puede modificar)
GRANT INSERT, UPDATE, DELETE ON 
    products, 
    product_localizations, 
    product_variants, 
    product_images, 
    catalog_products
TO pim_backend;

-- 6. PERMISOS EN SECUENCIAS
-- Cuando insertas un dato, PostgreSQL usa una 'secuencia' para generar el próximo ID (SERIAL).
-- El backend necesita permiso para usar esas secuencias al hacer un INSERT.
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO pim_backend;

-- Nota de Seguridad:
-- Debes asegurarte de que, al desplegar la aplicación, el script de conexión use
-- el usuario `pim_backend` para el código de la API.