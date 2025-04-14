# services/producto_service.py
from database import productos
from models.productos import Producto
def crear_producto(nombre, descripcion, precio, imagen):
 producto = Producto(nombre, descripcion, precio, imagen)
 productos.insert_one(producto.to_dict())
 print("Producto creado correctamente.")
def listar_productos():
 return productos.find()