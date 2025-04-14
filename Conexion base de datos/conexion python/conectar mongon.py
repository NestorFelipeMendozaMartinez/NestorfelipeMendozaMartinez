from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ecomerce3066478"]  # Nombre de la base de datos

# Crear colecciones
clientes = db["clientes1"]
productos = db["productos1"]
ventas = db["ventas"]
compras = db["compras1"]
comercio = db["comercio"]  # Corregí el nombre de la colección

# Insertar documentos de ejemplo
clientes.insert_one({
    "nombre": "Felipe Martinez",
    "correo": "mendozamartineznestorfelipe@gmail.com",
    "telefono": "3024018375",
    "direccion": "calle 16 N 12 B 44"
})

productos.insert_one({
    "nombre": "Felipe",
    "descripcion": "Laptop ASUSVivobook ",
    "precio": 9000,  # Corregí el valor del precio (sin punto decimal)
    "stock": 10  # Agregué el campo "stock" que faltaba
})
print("Base de datos y colecciones creadas en MongoDB")