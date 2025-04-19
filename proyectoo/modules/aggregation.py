from rich.console import Console  # Módulo para mejorar la presentación en consola
from rich.table import Table  # Módulo para crear tablas en consola
from rich.panel import Panel  # Módulo para crear paneles decorativos
from bson.json_util import dumps  # Módulo para serializar objetos BSON a JSON
import json  # Módulo para manejo de JSON
import random  # Módulo para generar datos aleatorios
from datetime import datetime  # Módulo para manejo de fechas

# Creación de una instancia de Console para la interfaz
console = Console()

def run(db):
    """
    Módulo de Pipeline de Agregación en MongoDB
    Args:
        db: Instancia de base de datos MongoDB
    Este módulo permite:
    - Ejecutar diferentes tipos de agregaciones
    - Aprender sobre pipelines de MongoDB
    - Realizar análisis de datos
    - Practicar con ejemplos reales
    """
    console.print(Panel.fit("🔢[bold cyan]Agregaciones en MongoDB[/bold cyan] 🔢"))
    
    # Verificar y crear datos de ejemplo si es necesario
    if "ventas" not in db.list_collection_names():
        console.print("\nℹ️ Creando colección 'ventas' con datos de ejemplo...")
        create_sample_sales_data(db)
    
    # Obtener referencia a la colección
    collection = db["ventas"]
    
    while True:
        # Crear tabla de menú con opciones disponibles
        table = Table(title="Operaciones de Agregación", show_header=True)
        table.add_column("Opción", style="cyan")
        table.add_column("Operación", style="green")
        table.add_column("Descripción", style="white")
        
        # Agregar opciones al menú
        table.add_row("1", "Agregación básica", "Ejemplo: Conteo y suma de ventas")
        table.add_row("2", "Agrupación por campo", "Agrupar por categoría/producto")
        table.add_row("3", "Filtros en pipelines", "Filtrar antes de agrupar")
        table.add_row("4", "Operadores avanzados", "Uso de $lookup, $unwind")
        table.add_row("5", "Pipeline personalizado", "Escribir tu propio pipeline")
        table.add_row("6", "Análisis temporal", "Agregaciones por fecha")
        table.add_row("7", "Estadísticas avanzadas", "Métricas y análisis detallado")
        table.add_row("0", "Volver", "Regresar al menú principal")
        console.print(table)

        choice = console.input("\n🔹Seleccione una operación (0-7): ")
        
        if choice == "0":
            break
        elif choice == "1":
            # Agregación básica: suma y conteo
            console.print("\n[bold]Agregación Básica:[/bold] Conteo y total de ventas")
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_ventas": {"$sum": "$monto"},
                        "cantidad_ventas": {"$sum": 1},
                        "promedio_venta": {"$avg": "$monto"},
                        "venta_minima": {"$min": "$monto"},
                        "venta_maxima": {"$max": "$monto"}
                    }
                }
            ]
            print_aggregation(collection, pipeline)
            
        elif choice == "2":
            # Agrupación por producto con métricas
            console.print("\n[bold]Agrupación por Producto:[/bold] Análisis detallado de ventas")
            pipeline = [
                {
                    "$group": {
                        "_id": "$producto",
                        "total_ventas": {"$sum": "$monto"},
                        "cantidad_ventas": {"$sum": 1},
                        "promedio_venta": {"$avg": "$monto"},
                        "venta_minima": {"$min": "$monto"},
                        "venta_maxima": {"$max": "$monto"}
                    }
                },
                {
                    "$project": {
                        "producto": "$_id",
                        "total_ventas": {"$round": ["$total_ventas", 2]},
                        "cantidad_ventas": 1,
                        "promedio_venta": {"$round": ["$promedio_venta", 2]},
                        "venta_minima": {"$round": ["$venta_minima", 2]},
                        "venta_maxima": {"$round": ["$venta_maxima", 2]}
                    }
                },
                {"$sort": {"total_ventas": -1}}
            ]
            print_aggregation(collection, pipeline)
            
        elif choice == "3":
            # Filtros avanzados con match y group
            console.print("\n[bold]Filtros en Pipeline:[/bold] Análisis de ventas filtradas")
            min_amount = float(console.input("Monto mínimo a filtrar: ") or "100")
            pipeline = [
                {
                    "$match": {
                        "monto": {"$gte": min_amount}
                    }
                },
                {
                    "$group": {
                        "_id": "$producto",
                        "total_ventas": {"$sum": "$monto"},
                        "cantidad_ventas": {"$sum": 1},
                        "promedio_venta": {"$avg": "$monto"}
                    }
                },
                {
                    "$project": {
                        "producto": "$_id",
                        "total_ventas": {"$round": ["$total_ventas", 2]},
                        "cantidad_ventas": 1,
                        "promedio_venta": {"$round": ["$promedio_venta", 2]}
                    }
                },
                {"$sort": {"total_ventas": -1}}
            ]
            print_aggregation(collection, pipeline)
            
        elif choice == "4":
            # Operadores avanzados con lookup y unwind
            console.print("\n[bold]Operadores Avanzados:[/bold] Join con productos")
            # Crear colección de productos si no existe
            if "productos" not in db.list_collection_names():
                productos = [
                    {"nombre": "Laptop", "categoria": "Tecnología", "proveedor": "TechCorp"},
                    {"nombre": "Smartphone", "categoria": "Tecnología", "proveedor": "MobileTech"},
                    {"nombre": "Camisa", "categoria": "Ropa", "proveedor": "FashionStyle"},
                    {"nombre": "Zapatos", "categoria": "Calzado", "proveedor": "FootWear"},
                    {"nombre": "Libro", "categoria": "Librería", "proveedor": "BookStore"}
                ]
                db["productos"].insert_many(productos)
                console.print("✅[green]Colección 'productos' creada[/green]")
                
            pipeline = [
                {
                    "$lookup": {
                        "from": "productos",
                        "localField": "producto",
                        "foreignField": "nombre",
                        "as": "info_producto"
                    }
                },
                {"$unwind": "$info_producto"},
                {
                    "$group": {
                        "_id": {
                            "categoria": "$info_producto.categoria",
                            "proveedor": "$info_producto.proveedor"
                        },
                        "total_ventas": {"$sum": "$monto"},
                        "cantidad_ventas": {"$sum": 1}
                    }
                },
                {
                    "$project": {
                        "categoria": "$_id.categoria",
                        "proveedor": "$_id.proveedor",
                        "total_ventas": {"$round": ["$total_ventas", 2]},
                        "cantidad_ventas": 1
                    }
                },
                {"$sort": {"total_ventas": -1}}
            ]
            print_aggregation(collection, pipeline)
            
        elif choice == "5":
            # Pipeline personalizado con validación
            console.print("\n[bold]Pipeline Personalizado:[/bold]")
            console.print("""
            Ejemplo de pipeline:
            [
                {"$match": {"producto": "Laptop"}},
                {"$group": {
                    "_id": null,
                    "total": {"$sum": "$monto"},
                    "cantidad": {"$sum": 1}
                }}
            ]
            """)
            try:
                pipeline_input = console.input("Ingresa el pipeline (formato JSON): ")
                pipeline = json.loads(pipeline_input)
                print_aggregation(collection, pipeline)
            except Exception as e:
                console.print(f"\n❌[red]Error en el pipeline: {e}[/red]")
                
        elif choice == "6":
            # Análisis temporal de ventas
            console.print("\n[bold]Análisis Temporal:[/bold] Ventas por período")
            pipeline = [
                {
                    "$group": {
                        "_id": {
                            "año_mes": {"$substr": ["$fecha", 0, 7]},
                            "producto": "$producto"
                        },
                        "total_ventas": {"$sum": "$monto"},
                        "cantidad_ventas": {"$sum": 1}
                    }
                },
                {
                    "$project": {
                        "periodo": "$_id.año_mes",
                        "producto": "$_id.producto",
                        "total_ventas": {"$round": ["$total_ventas", 2]},
                        "cantidad_ventas": 1
                    }
                },
                {"$sort": {"periodo": 1, "total_ventas": -1}}
            ]
            print_aggregation(collection, pipeline)
            
        elif choice == "7":
            # Estadísticas avanzadas
            console.print("\n[bold]Estadísticas Avanzadas:[/bold] Análisis detallado")
            pipeline = [
                {
                    "$facet": {
                        "por_producto": [
                            {"$group": {
                                "_id": "$producto",
                                "total": {"$sum": "$monto"},
                                "cantidad": {"$sum": 1}
                            }},
                            {"$sort": {"total": -1}}
                        ],
                        "por_metodo_pago": [
                            {"$group": {
                                "_id": "$metodo_pago",
                                "total": {"$sum": "$monto"},
                                "cantidad": {"$sum": 1}
                            }}
                        ],
                        "estadisticas_generales": [
                            {"$group": {
                                "_id": None,
                                "total_ventas": {"$sum": "$monto"},
                                "promedio_venta": {"$avg": "$monto"},
                                "venta_maxima": {"$max": "$monto"},
                                "venta_minima": {"$min": "$monto"}
                            }}
                        ]
                    }
                }
            ]
            print_aggregation(collection, pipeline)
            
        else:
            console.print("\n❌[red]Opción inválida. Intente nuevamente.[/red]")
        
        console.input("\nPresione Enter para continuar...")
        console.clear()

def print_aggregation(collection, pipeline):
    """
    Ejecuta y muestra resultados de un pipeline de agregación
    Args:
        collection: Colección de MongoDB
        pipeline: Lista de etapas del pipeline de agregación
    """
    console.print("\n[bold]Pipeline ejecutado:[/bold]")
    console.print(dumps(pipeline, indent=2))
    
    try:
        results = list(collection.aggregate(pipeline))
        if not results:
            console.print("\nℹ️ No se encontraron resultados")
            return
        
        # Crear tabla con los resultados
        table = Table(title="Resultados de Agregación", show_header=True)
        
        # Obtener las claves del primer documento para las columnas
        for key in results[0].keys():
            if key != "_id":  # Excluir el campo _id
                table.add_column(str(key))
        
        # Agregar filas con los resultados
        for doc in results:
            row_data = []
            for key in doc.keys():
                if key != "_id":  # Excluir el campo _id
                    value = doc[key]
                    if isinstance(value, (int, float)):
                        value = f"{value:,.2f}"
                    row_data.append(str(value))
            table.add_row(*row_data)
        
        console.print(table)
        
        # Mostrar resumen si hay múltiples resultados
        if len(results) > 1:
            console.print(f"\nTotal de resultados: {len(results)}")
            
    except Exception as e:
        console.print(f"\n❌[red]Error en agregación: {e}[/red]")

def create_sample_sales_data(db):
    """
    Crea datos de ejemplo para el módulo de agregación
    Args:
        db: Instancia de base de datos MongoDB
    """
    # Datos de ejemplo
    productos = ["Laptop", "Smartphone", "Camisa", "Zapatos", "Libro"]
    vendedores = [f"Vendedor-{i}" for i in range(1, 6)]
    metodos_pago = ["Tarjeta", "Efectivo", "Transferencia", "Crypto", "PayPal"]
    ventas = []
    
    # Generar 1000 ventas aleatorias
    for _ in range(1000):
        fecha = datetime(2023, random.randint(1, 12), random.randint(1, 28))
        venta = {
            "producto": random.choice(productos),
            "monto": round(random.uniform(10, 1000), 2),
            "fecha": fecha.strftime("%Y-%m-%d"),
            "vendedor": random.choice(vendedores),
            "metodo_pago": random.choice(metodos_pago),
            "cantidad": random.randint(1, 5),
            "descuento": random.choice([0, 5, 10, 15, 20])
        }
        ventas.append(venta)
    
    # Insertar ventas en la colección
    db["ventas"].insert_many(ventas)
    console.print(f"✅[green]Insertadas {len(ventas)} ventas de ejemplo[/green]")