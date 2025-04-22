from bson import ObjectId
try:
    ObjectId("605c72b44f1c2f1d4c8b4567")  # No lanza error = ID válido
    print("✅ ID válido")
except:
    print("❌ ID inválido")