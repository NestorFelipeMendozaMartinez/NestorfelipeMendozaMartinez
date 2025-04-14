class Inventario:
   def __init__(self, producto_id, cantidad):
    self.producto_id =producto_id
    self.cantidad = cantidad
    def to_dict(self):
     return {
       "producto_id": self.producto_id,
       "cantidad": self.cantidad
 }