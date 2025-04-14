class Producto:
  def __init__(self, nombre, descripcion, precio, imagen):
   self.nombre = nombre
   self.descripcion = descripcion
   self.precio = precio
   self.imagen = imagen # Ruta de la imagen
def to_dict(self):
  return {
    "nombre": self.nombre,
    "descripcion": self.descripcion,
    "precio": self.precio,
    "imagen": self.imagen
    }