import mysql.connector

try:
    # Conectar a MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456"
    )
    cursor = conn.cursor()

    # Crear la base de datos
    cursor.execute("CREATE DATABASE IF NOT EXISTS ecomer3066478")

    # Conectar a la base de datos
    conn.database = "ecomer3066478"

    # Crear tablas
    tables = {
        "clientes": """
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255),
            correo VARCHAR(255),
            telefono VARCHAR(20),
            direccion TEXT
        );
        """,
        "productos": """
        CREATE TABLE IF NOT EXISTS productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255),
            descripcion TEXT,
            precio DECIMAL(10, 2),
            stock INT
        );
        """,
        "ventas": """
        CREATE TABLE IF NOT EXISTS ventas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total DECIMAL(10, 2),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );
        """,
        "detalle_ventas": """
        CREATE TABLE IF NOT EXISTS detalle_ventas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            venta_id INT,
            producto_id INT,
            cantidad INT,
            subtotal DECIMAL(10, 2),
            FOREIGN KEY (venta_id) REFERENCES ventas(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        );
        """,
        "compras": """
        CREATE TABLE IF NOT EXISTS compras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total DECIMAL(10, 2)
        );
        """
    }

    # Ejecutar las consultas para crear las tablas
    for name, query in tables.items():
        cursor.execute(query)
        print(f"Tabla '{name}' creada correctamente.")

    # Confirmar los cambios
    conn.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Cerrar el cursor y la conexión
    if cursor:
        cursor.close()
    if conn:
        conn.close()