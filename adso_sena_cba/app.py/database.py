import pymongo
# Conexión a MongoDB
cliente = pymongo.MongoClient("mongodb://localhost:27017/")
db = cliente['adso_sena_cba'] # Nombre de la base de datos
# Colecciones
usuarios = db['usuarios'] # Usuarios (clientes y empleados)
productos = db['productos'] # Productos de la tienda
inventarios = db['inventarios'] # Inventario de productos
ventas = db['ventas'] # Registro de ventas

print("✅ Conexión exitosa a la base de datos.")