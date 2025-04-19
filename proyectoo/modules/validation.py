from rich.console import Console  # Módulo para mejorar la presentación en consola
from rich.table import Table  # Módulo para crear tablas en consola
from rich.panel import Panel  # Módulo para crear paneles decorativos
from bson.son import SON  # Módulo para crear objetos BSON ordenados

# Creación de una instancia de Console para la interfaz
console = Console()

def run(db):
    """
    Módulo de validación de esquemas en MongoDB
    Args:
        db: Instancia de base de datos MongoDB
    Este módulo permite:
    - Ver y modificar reglas de validación
    - Crear esquemas de validación
    - Probar la validación con documentos
    """
    console.print(Panel.fit("🔍[bold cyan]Validación de Esquemas en MongoDB[/bold cyan] 🔍"))
    
    # Obtener o crear una colección para trabajar
    collections = db.list_collection_names()  # Método que lista todas las colecciones
    
    if not collections:
        collection_name = "validated_users"
        # create_collection() - Método para crear una nueva colección
        db.create_collection(collection_name)
    else:
        collection_name = console.input(f"\nIngrese el nombre de la colección ({', '.join(collections)}): ")
    
    # Obtener referencia a la colección
    collection = db[collection_name]
    
    while True:
        # Crear tabla de menú con opciones disponibles
        table = Table(title="Operaciones de Validación", show_header=True)
        table.add_column("Opción", style="cyan")
        table.add_column("Operación", style="green")
        table.add_column("Descripción", style="white")
        
        # Agregar opciones al menú
        table.add_row("1", "Mostrar reglas actuales", "Ver las reglas de validación existentes")
        table.add_row("2", "Agregar validación simple", "Añadir validación básica a la colección")
        table.add_row("3", "Agregar validación JSON Schema", "Añadir validación con esquema JSON")
        table.add_row("4", "Eliminar validación", "Remover todas las reglas de validación")
        table.add_row("5", "Probar validación", "Insertar documentos para probar las reglas")
        table.add_row("0", "Volver", "Regresar al menú principal")
        console.print(table)

        choice = console.input("\n🔹Seleccione una operación (0-5): ")
        
        if choice == "0":
            break
            
        elif choice == "1":
            # Mostrar reglas de validación actuales
            console.print("\n[bold]Reglas de validación actuales:[/bold]")
            try:
                # command() - Método para ejecutar comandos de administración
                info = db.command(SON([("listCollections", 1)]))["cursor"]["firstBatch"]
                coll_info = next((c for c in info if c["name"] == collection_name), None)
                
                if coll_info and "options" in coll_info and "validator" in coll_info["options"]:
                    validator = coll_info["options"]["validator"]
                    validation_level = coll_info["options"].get("validationLevel", "strict")
                    validation_action = coll_info["options"].get("validationAction", "error")
                    
                    console.print(f"\n🔹[bold]Nivel de validación:[/bold] {validation_level}")
                    console.print(f"🔹[bold]Acción de validación:[/bold] {validation_action}")
                    console.print("\n[bold]Reglas del validador:[/bold]")
                    console.print(validator)
                else:
                    console.print("\nℹ️ No hay reglas de validación definidas para esta colección")
            except Exception as e:
                console.print(f"\n❌[red]Error al obtener reglas: {e}[/red]")
                
        elif choice == "2":
            # Agregar validación simple usando operadores de MongoDB
            console.print("\n[bold]Agregar validación simple[/bold]")
            console.print("Ejemplo: {'age': {'$gte': 18}, 'email': {'$regex': '@example\\.com$'}}")
            validator_input = console.input("Ingrese las reglas de validación (en formato JSON): ")
            
            try:
                validator = eval(validator_input)  # Convertir string a diccionario
                validation_level = console.input("Nivel de validación (strict/off) [strict]: ") or "strict"
                validation_action = console.input("Acción de validación (error/warn) [error]: ") or "error"
                
                # collMod - Comando para modificar una colección
                db.command({
                    "collMod": collection_name,
                    "validator": validator,
                    "validationLevel": validation_level,
                    "validationAction": validation_action
                })
                console.print("\n✅[green]Reglas de validación actualizadas correctamente[/green]")
            except Exception as e:
                console.print(f"\n❌[red]Error al actualizar validación: {e}[/red]")
                
        elif choice == "3":
            # Agregar validación usando JSON Schema
            console.print("\n[bold]Agregar validación con JSON Schema[/bold]")
            console.print("Ejemplo de esquema:")
            console.print("""{
    "bsonType": "object",
    "required": ["name", "email", "age"],
    "properties": {
        "name": {"bsonType": "string"},
        "email": {"bsonType": "string", "pattern": "^\\S+@\\S+\\.\\S+$"},
        "age": {"bsonType": "int", "minimum": 18}
    }
}""")
            schema_input = console.input("Ingrese el esquema JSON: ")
            
            try:
                schema = eval(schema_input)
                validation_level = console.input("Nivel de validación (strict/off) [strict]: ") or "strict"
                validation_action = console.input("Acción de validación (error/warn) [error]: ") or "error"
                
                # $jsonSchema - Operador para definir un esquema de validación JSON
                db.command({
                    "collMod": collection_name,
                    "validator": {"$jsonSchema": schema},
                    "validationLevel": validation_level,
                    "validationAction": validation_action
                })
                console.print("\n✅[green]Esquema JSON de validación actualizado correctamente[/green]")
            except Exception as e:
                console.print(f"\n❌[red]Error al actualizar esquema: {e}[/red]")
                
        elif choice == "4":
            # Eliminar todas las reglas de validación
            console.print("\n[bold]Eliminar validación[/bold]")
            confirm = console.input("¿Está seguro de eliminar todas las reglas de validación? (s/n): ")
            
            if confirm.lower() == "s":
                try:
                    db.command({
                        "collMod": collection_name,
                        "validator": {},  # Validator vacío elimina las reglas
                        "validationLevel": "off"
                    })
                    console.print("\n✅[green]Reglas de validación eliminadas correctamente[/green]")
                except Exception as e:
                    console.print(f"\n❌[red]Error al eliminar validación: {e}[/red]")
                    
        elif choice == "5":
            # Probar las reglas de validación
            console.print("\n[bold]Probar validación[/bold]")
            console.print("1. Insertar documento válido\n2. Insertar documento inválido")
            test_choice = console.input("Seleccione opción (1-2): ")
            
            if test_choice == "1":
                console.print("\nIngrese un documento que cumpla con las reglas de validación")
                doc_input = console.input("Documento (en formato JSON): ")
                
                try:
                    doc = eval(doc_input)
                    # insert_one() - Método para insertar un documento
                    result = collection.insert_one(doc)
                    console.print(f"\n✅[green]Documento insertado correctamente con _id: {result.inserted_id}[/green]")
                except Exception as e:
                    console.print(f"\n❌[red]Error al insertar documento: {e}[/red]")
                    
            elif test_choice == "2":
                console.print("\nIngrese un documento que viole las reglas de validación")
                doc_input = console.input("Documento (en formato JSON): ")
                
                try:
                    doc = eval(doc_input)
                    result = collection.insert_one(doc)
                    console.print("\n⚠️[yellow]Documento insertado a pesar de las reglas (puede ser por nivel 'warn')[/yellow]")
                except Exception as e:
                    console.print(f"\n❌[red]Error de validación (esperado): {e}[/red]")
                    
        else:
            console.print("\n❌[red]Opción inválida. Intente nuevamente.[/red]")
        
        console.input("\nPresione Enter para continuar...")
        console.clear()