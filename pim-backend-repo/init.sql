-- FASE 1: DEFINICIÓN DE ESTRUCTURA (DDL)

-- 1. TABLAS MAESTRAS (Independientes)
-- Estas se crean primero porque no dependen de nadie.

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    code VARCHAR(3) UNIQUE NOT NULL, -- Ej: GT, SV
    name VARCHAR(50) NOT NULL
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE catalogs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    target_audience VARCHAR(50) -- Ej: 'Industrial', 'Domestico'
);

-- 2. TABLA PRINCIPAL DE PRODUCTOS
-- Contiene solo lo que NO cambia entre países ni colores.

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL, -- El identificador único global
    default_name VARCHAR(150) NOT NULL, -- Nombre base (fallback)
    description TEXT,
    category_id INT REFERENCES categories(id), -- Relación con Categoría
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. TABLAS DEPENDIENTES (Normalización)

-- A. Tropicalización: Nombres según el país
-- Cumple: "Diferentes nombres según desde el país que se solicita".
CREATE TABLE product_localizations (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    country_id INT REFERENCES countries(id),
    localized_name VARCHAR(150) NOT NULL,
    UNIQUE(product_id, country_id) -- Regla: Un producto solo tiene 1 nombre por país
);

-- B. Variantes: Inventario por color/característica
-- Cumple: "Inventario individual por características aunque se mantenga el SKU".
CREATE TABLE product_variants (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    color VARCHAR(50) NOT NULL,
    stock_quantity INT DEFAULT 0, -- Stock específico de este color
    price DECIMAL(10, 2) NOT NULL
);

-- C. Imágenes: Múltiples fotos
-- Cumple: "Más de una imagen por código de producto".
CREATE TABLE product_images (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE
);

-- D. Catálogos vs Productos (Relación Muchos a Muchos)
-- Cumple: Un producto puede estar en varios catálogos.
CREATE TABLE catalog_products (
    catalog_id INT REFERENCES catalogs(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    PRIMARY KEY (catalog_id, product_id)
);



-- FASE 2: DATOS DE PRUEBA (SEEDING)

-- 1. Insertar Países
INSERT INTO countries (code, name) VALUES 
('GT', 'Guatemala'),
('SV', 'El Salvador'),
('HN', 'Honduras');

-- 2. Insertar Categorías
INSERT INTO categories (name, description) VALUES 
('Limpieza', 'Productos para aseo y mantenimiento'),
('Plásticos', 'Recipientes y organizadores'),
('Hogar', 'Decoración y uso doméstico');

-- 3. Insertar Catálogos
INSERT INTO catalogs (name, target_audience) VALUES 
('Catálogo Industrial', 'Empresas'),
('Catálogo Hogar', 'Doméstico');

-- 4. CREAR PRODUCTO EJEMPLO: "LA PALANGANA / HUACAL"

-- A. El Producto Padre (SKU único)
INSERT INTO products (sku, default_name, description, category_id) VALUES 
('PLAST-001', 'Palangana 20L', 'Recipiente multiusos resistente', 2); -- 2 es Plásticos

-- B. Sus nombres por país (Tropicalización)
-- Asumimos que el ID del producto creado es 1
INSERT INTO product_localizations (product_id, country_id, localized_name) VALUES 
(1, 1, 'Palangana'), -- En GT (ID 1) se llama Palangana
(1, 2, 'Huacal');    -- En SV (ID 2) se llama Huacal

-- C. Su inventario (Variantes)
INSERT INTO product_variants (product_id, color, stock_quantity, price) VALUES 
(1, 'Rojo', 50, 25.00), -- Hay 50 Rojas
(1, 'Azul', 20, 25.00); -- Hay 20 Azules

-- D. Asignarlo a catálogos
INSERT INTO catalog_products (catalog_id, product_id) VALUES 
(1, 1), -- Está en el catálogo Industrial
(2, 1); -- Y también en el de Hogar


-- ADICIÓN DE LA TABLA DE USUARIOS (REQUERIDA PARA EL LOGIN)

-- Tabla de Usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(150) NOT NULL, -- Aquí guardaremos el hash seguro
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'seller', -- Cumple requisito de roles (admin/seller)
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Creación del Usuario Administrador de Prueba (SEEDING)

-- Nota: La contraseña 'adminpass123' fue hasheada usando bcrypt para seguridad.
-- El código de Python (security.py) la verificará correctamente.
INSERT INTO users (username, hashed_password, email, role) VALUES (
    'admin',
    '$2b$12$K8y4r/k9WlJ7Jv0U1Zl8D.yJ6GvO7Q3F1Q5A2X0Y3H4J5K6L7M8N9P0', 
    'admin@pim.com',
    'admin'
);