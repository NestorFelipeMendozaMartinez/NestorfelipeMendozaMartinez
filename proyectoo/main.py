from dotenv import load_dotenv
from pymongo import MongoClient
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import os  # Added missing import for environment variables

# Importar módulos locales
from modules import validation
from modules import transactions
from modules import indexes

# Consola enriquecida
console = Console()

# ---------------- FUNCIONES CRUD ---------------- #
def insert_document(collection):
    """Insertar un documento en la colección"""
    console.print("\n[bold cyan]Insertar Documento[/bold cyan]")
    nombre = console.input("Nombre: ")
    correo = console.input("Correo electrónico: ")
    edad = console.input("Edad: ")
    documento = {"nombre": nombre, "correo": correo, "edad": int(edad)}
    resultado = collection.insert_one(documento)
    console.print(f"[green]✓ Documento insertado con ID:[/green] {resultado.inserted_id}")

def find_documents(collection):
    """Buscar documentos en la colección"""
    console.print("\n[bold cyan]Buscar Documentos[/bold cyan]")
    documentos = collection.find()
    tabla = Table(title="Usuarios encontrados", show_lines=True)
    tabla.add_column("ID", style="magenta")
    tabla.add_column("Nombre", style="cyan")
    tabla.add_column("Correo", style="green")
    tabla.add_column("Edad", style="yellow")
    for doc in documentos:
        tabla.add_row(
            str(doc.get("_id")),
            doc.get("nombre", "N/A"),
            doc.get("correo", "N/A"),
            str(doc.get("edad", "N/A"))
        )
    console.print(tabla)

def update_document(collection):
    """Actualizar un documento existente"""
    console.print("\n[bold cyan]Actualizar Documento[/bold cyan]")
    correo = console.input("Correo del usuario a actualizar: ")
    nuevo_nombre = console.input("Nuevo nombre: ")
    nueva_edad = console.input("Nueva edad: ")
    resultado = collection.update_one(
        {"correo": correo},
        {"$set": {"nombre": nuevo_nombre, "edad": int(nueva_edad)}}
    )
    if resultado.modified_count > 0:
        console.print("[green]✓ Documento actualizado correctamente[/green]")
    else:
        console.print("[yellow]No se encontró ningún documento con ese correo[/yellow]")

def delete_document(collection):
    """Eliminar un documento existente"""
    console.print("\n[bold cyan]Eliminar Documento[/bold cyan]")
    correo = console.input("Correo del usuario a eliminar: ")
    resultado = collection.delete_one({"correo": correo})
    if resultado.deleted_count > 0:
        console.print("[red]✓ Documento eliminado correctamente[/red]")
    else:
        console.print("[yellow]No se encontró ningún documento con ese correo[/yellow]")

# ---------------- MENÚ PRINCIPAL ---------------- #
def show_menu():
    """Muestra el menú principal"""
    console.print(Panel.fit("📚[bold cyan]Aprende MongoDB con Python[/bold cyan] 📚"))
    menu = Table(title="Módulos Disponibles", show_header=True, header_style="bold magenta")
    menu.add_column("Opción", style="cyan")
    menu.add_column("Operación", style="green")
    menu.add_column("Descripción", style="white")

    menu.add_row("1", "Insertar Documento", "Aprende a insertar documentos en MongoDB")
    menu.add_row("2", "Buscar Documentos", "Realizar consultas en la base de datos")
    menu.add_row("3", "Actualizar Documento", "Modificar documentos existentes")
    menu.add_row("4", "Eliminar Documento", "Eliminar documentos de la colección")
    menu.add_row("5", "Validación de Esquemas", "Gestionar reglas de validación")
    menu.add_row("6", "Transacciones", "Operaciones transaccionales ACID")
    menu.add_row("7", "Índices", "Gestión y análisis de índices")
    menu.add_row("0", "Salir", "Terminar el programa")
    console.print(menu)

# ---------------- EJECUCIÓN PRINCIPAL ---------------- #
def main():
    """Función principal que ejecuta la aplicación"""
    load_dotenv()  # Cargar variables de entorno
    try:
        # Establecer conexión con MongoDB
        client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
        client.admin.command("ping")  # Validar conexión
        db = client[os.getenv("DB_NAME", "tutorial_db")]
        collection = db["usuarios"]
        console.print("[green]✓ Conexión exitosa a MongoDB[/green]")

        # Diccionario de operaciones disponibles
        operations = {
            "1": lambda: insert_document(collection),
            "2": lambda: find_documents(collection),
            "3": lambda: update_document(collection),
            "4": lambda: delete_document(collection),
            "5": lambda: validation.run(db),
            "6": lambda: transactions.run(db),
            "7": lambda: indexes.run(db)
        }

        while True:
            show_menu()
            choice = console.input("\n[cyan]Seleccione una opción (0-7): [/cyan]")
            if choice == "0":
                console.print("\n[yellow]¡Hasta luego![/yellow]")
                break
            if choice in operations:
                operations[choice]()
                console.input("\nPresione Enter para continuar...")
                console.clear()
            else:
                console.print("\n[red]Opción inválida. Intente nuevamente.[/red]")
    except Exception as e:
        console.print(f"[red]Error de conexión: {e}[/red]")

if __name__ == "__main__":
    main()