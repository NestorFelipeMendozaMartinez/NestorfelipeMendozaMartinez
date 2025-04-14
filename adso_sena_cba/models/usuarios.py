# models/usuarios.py
class Usuario:
  def __init__(self, nombre, email, password, rol):
   self.nombre = nombre
   self.email = email
   self.password = password
   self.rol = rol # Rol: cliente o empleado
def to_dict(self):
  return {
 "nombre": self.nombre,
 "email": self.email,
  "password": self.password,
  "rol": self.rol
 }