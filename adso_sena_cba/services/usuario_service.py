from database import usuarios
from models.usuarios import Usuario
def crear_usuario(nombre, email, password, rol):
  usuario = Usuario(nombre, email, password, rol)
  usuarios.insert_one(usuario.to_dict())
  print("Usuario creado correctamente.")
def buscar_usuario(email):
  return usuarios.find_one({"email": email})
def login(email, password):
  usuario = buscar_usuario(email)
  if usuario and usuario["password"] == password:
     print("Login exitoso.")
     return usuario
  else:
     print("Credenciales incorrectas.")
     return None