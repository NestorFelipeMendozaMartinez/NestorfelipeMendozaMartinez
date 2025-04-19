from pymongo import MongoClient

# 1. Conectar a MongoDB (asegúrate de tener el servicio corriendo)
client = MongoClient('mongodb://localhost:27017/')

# 2. Seleccionar la base de datos (si no existe, se crea al insertar)
db = client['mi_tienda']

# 3. Crear la colección 'clientes' e insertar documentos
clientes = db['clientes']

# Insertar los 3 documentos
clientes.insert_many([
    {
        "nombre": "Juan Pérez",
        "ciudad": "Mosquera",
        "compras": [120.50, 45.99, 78.30]
    },
    {
        "nombre": "María García",
        "ciudad": "funza",
        "compras": [95.20, 34.50]
    },
    {
        "nombre": "Carlos López",
        "ciudad": "Madrid",
        "compras": [210.00, 56.75, 89.90, 125.30]
    }
])

# 4. Consultar clientes con más de 2 compras
resultados = clientes.find({
    "$expr": {
        "$gt": [
            {"$size": "$compras"},
            2
        ]
    }
})

# Mostrar resultados (CORRECCIÓN: paréntesis cerrado)
print("Clientes con más de 2 compras:")
for cliente in resultados:
    print(f"Nombre: {cliente['nombre']}, Ciudad: {cliente['ciudad']}, Compras: {len(cliente['compras'])}")