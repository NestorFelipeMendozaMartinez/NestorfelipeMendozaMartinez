import  psycopg2

# Conectar a PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123456",
    host="localhost"

)
conn.autocommit = True  # Habilitar autocommit
cursor = conn.cursor()

# Crear base de datos
cursor.execute("CREATE DATABASE ecommerce3066478")
conn.close()  # Cerrar conexión para conectar a la nueva base

# Conectar a la base de datos recién creada
conn = psycopg2.connect(
    dbname="ecommerce3066478",
    user="postgres",
    password="123456",
    host="localhost"
)
cursor = conn.cursor()

# Crear tablas
tables = {
    "clientes": """
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255),
            correo VARCHAR(255) UNIQUE,
            telefono VARCHAR(20),
            direccion TEXT
        )
    """,
    "productos": """
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255),
            descripcion TEXT,
            precio DECIMAL(10,2),
            stock INT
        )
    """,
    "ventas": """
        CREATE TABLE IF NOT EXISTS ventas (
            id SERIAL PRIMARY KEY,
            cliente_id INT REFERENCES clientes(id),
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total DECIMAL(10,2)
        )
    """,
    "detalle_ventas": """
        CREATE TABLE IF NOT EXISTS detalle_ventas (
            id SERIAL PRIMARY KEY,
            venta_id INT REFERENCES ventas(id),
            producto_id INT REFERENCES productos(id),
            cantidad INT,
            subtotal DECIMAL(10,2)
        )
    """,
    "compras": """
        CREATE TABLE IF NOT EXISTS compras (
            id SERIAL PRIMARY KEY,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total DECIMAL(10,2)
        )
    """,
    "detalle_compras": """
        CREATE TABLE IF NOT EXISTS detalle_compras (
            id SERIAL PRIMARY KEY,
            compra_id INT REFERENCES compras(id),
            producto_id INT REFERENCES productos(id),
            cantidad INT,
            costo DECIMAL(10,2)
        )
    """
}

# Ejecutar las consultas para crear las tablas
for name, query in tables.items():
    cursor.execute(query)
    print(f"Tabla {name} creada correctamente.")

# Guardar los cambios y cerrar la conexión
conn.commit()
cursor.close()
conn.close()