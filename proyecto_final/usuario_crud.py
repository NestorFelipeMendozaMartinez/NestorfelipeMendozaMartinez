from bson import ObjectId
from datetime import datetime
from mongo_conexion import obtener_db


def obtener_usuario_por_id(id):
    db = obtener_db()
    return db.usuarios.find_one({"_id": ObjectId(id)})


def obtener_usuario_por_email(email):
    db = obtener_db()
    return db.usuarios.find_one({"email": email})


def crear_usuario(nombre, email, contrasena, rol="cliente"):
    db = obtener_db()
    usuario = {
        "nombre": nombre,
        "email": email,
        "contrasena": contrasena,
        "rol": rol,
        "fechaRegistro": datetime.now()
    }
    resultado = db.usuarios.insert_one(usuario)
    return obtener_usuario_por_id(resultado.inserted_id)


def actualizar_usuario(id, nuevos_datos):
    db = obtener_db()
    db.usuarios.update_one(
        {"_id": ObjectId(id)},
        {"$set": nuevos_datos}
    )
    return obtener_usuario_por_id(id)


def eliminar_usuario(id):
    db = obtener_db()
    return db.usuarios.delete_one({"_id": ObjectId(id)}).deleted_count == 1