from rich.console import Console  # Módulo para mejorar la presentación en consola
from rich.table import Table  # Módulo para crear tablas en consola
from rich.panel import Panel  # Módulo para crear paneles decorativos
from bson.objectid import ObjectId  # Módulo para manejar ObjectId de MongoDB

# Creación de una instancia de Console para la interfaz
console = Console()

def try_eval(value):
    """
    Intenta evaluar el input como expresión Python, sino lo deja como string
    Args:
        value: Valor a evaluar
    Returns:
        El valor evaluado si es posible, sino el string original
    """
    try:
        return eval(value)
    except:
        return value

def print_documents(docs):
    """
    Muestra documentos en una tabla formateada
    Args:
        docs: Lista de documentos a mostrar
    """
    if not docs:
        console.print("\nℹ️ No se encontraron documentos")
        return
    
    # Crear tabla con las claves del primer documento
    table = Table(title="Documentos Encontrados", show_header=True)
    for key in docs[0].keys():
        table.add_column(str(key))
    
    # Agregar filas con los valores de cada documento
    for doc in docs:
        row = []
        for val in doc.values():
            # Convertir ObjectId a string para mostrar
            if isinstance(val, ObjectId):
                row.append(str(val))
            else:
                row.append(str(val))
        table.add_row(*row)
    
    console.print(table)

def run(db):
    """
    Módulo de operaciones CRUD en MongoDB
    Args:
        db: Instancia de base de datos MongoDB
    Este módulo permite:
    - Crear (Create) documentos
    - Leer (Read) documentos
    - Actualizar (Update) documentos
    - Eliminar (Delete) documentos
    - Contar documentos
    """
    console.print(Panel.fit("📝[bold cyan]Operaciones CRUD en MongoDB[/bold cyan] 📝"))
    
    # Seleccionar o crear colección
    collections = db.list_collection_names()  # Método que lista todas las colecciones
    
    if not collections:
        console.print("\nℹ️ No hay colecciones en esta base de datos. Creando una nueva...")
        collection_name = "ejemplo_crud"
        # create_collection() - Método para crear una nueva colección
        db.create_collection(collection_name)
    else:
        collection_name = console.input(f"\nIngrese el nombre de la colección ({', '.join(collections)}): ")
    
    # Obtener referencia a la colección
    collection = db[collection_name]
    
    while True:
        # Mostrar menú de operaciones CRUD
        table = Table(title="Operaciones CRUD", show_header=True)
        table.add_column("Opción", style="cyan")
        table.add_column("Operación", style="green")
        table.add_column("Descripción", style="white")
        
        # Agregar opciones al menú
        table.add_row("1", "Insertar", "Agregar nuevos documentos")
        table.add_row("2", "Buscar", "Consultar documentos")
        table.add_row("3", "Actualizar", "Modificar documentos")
        table.add_row("4", "Eliminar", "Borrar documentos")
        table.add_row("5", "Conteo", "Contar documentos")
        table.add_row("0", "Volver", "Regresar al menú principal")
        console.print(table)

        choice = console.input("\n🔹Seleccione una operación CRUD (0-5): ")
        
        if choice == "0":
            break
            
        elif choice == "1":
            # Operaciones de inserción (Create)
            console.print("\n[bold]Insertar documentos[/bold]")
            console.print("1. Insertar uno\n2. Insertar varios")
            insert_choice = console.input("Seleccione opción (1-2): ")
            
            if insert_choice == "1":
                # insert_one() - Método para insertar un documento
                doc = {}
                while True:
                    key = console.input("Ingrese clave (o dejar vacío para terminar): ")
                    if not key:
                        break
                    value = console.input(f"Ingrese valor para '{key}': ")
                    doc[key] = try_eval(value)
                
                if doc:
                    result = collection.insert_one(doc)
                    console.print(f"\n✅[green]Documento insertado con ID: {result.inserted_id}[/green]")
                else:
                    console.print("\n❌[red]No se proporcionaron datos para insertar[/red]")
                    
            elif insert_choice == "2":
                # insert_many() - Método para insertar múltiples documentos
                docs = []
                console.print("\nIngrese documentos (deje vacío para terminar):")
                
                while True:
                    doc = {}
                    console.print(f"\nDocumento #{len(docs) + 1}:")
                    
                    while True:
                        key = console.input("Ingrese clave (o dejar vacío para terminar documento): ")
                        if not key:
                            break
                        value = console.input(f"Ingrese valor para '{key}': ")
                        doc[key] = try_eval(value)
                    
                    if doc:
                        docs.append(doc)
                    else:
                        break
                
                if docs:
                    result = collection.insert_many(docs)
                    console.print(f"\n✅[green]Insertados {len(result.inserted_ids)} documentos[/green]")
                    console.print(f"IDs: {result.inserted_ids}")
                else:
                    console.print("\n❌[red]No se proporcionaron documentos para insertar[/red]")
                    
        elif choice == "2":
            # Operaciones de búsqueda (Read)
            console.print("\n[bold]Buscar documentos[/bold]")
            console.print("1. Buscar todos\n2. Buscar con filtro\n3. Buscar uno")
            find_choice = console.input("Seleccione opción (1-3): ")
            
            if find_choice == "1":
                # find() - Método para buscar múltiples documentos
                docs = list(collection.find())
                print_documents(docs)
                
            elif find_choice == "2":
                try:
                    query = console.input("Ingrese filtro (ej: {'nombre': 'Juan'}): ")
                    query = eval(query) if query else {}
                    docs = list(collection.find(query))
                    print_documents(docs)
                except Exception as e:
                    console.print(f"\n❌[red]Error en la consulta: {e}[/red]")
                    
            elif find_choice == "3":
                # find_one() - Método para buscar un solo documento
                try:
                    query = console.input("Ingrese filtro (ej: {'_id': ObjectId('...')}): ")
                    query = eval(query) if query else {}
                    doc = collection.find_one(query)
                    
                    if doc:
                        print_documents([doc])
                    else:
                        console.print("\nℹ️ No se encontraron documentos")
                except Exception as e:
                    console.print(f"\n❌[red]Error en la consulta: {e}[/red]")
                    
        elif choice == "3":
            # Operaciones de actualización (Update)
            console.print("\n[bold]Actualizar documentos[/bold]")
            console.print("1. Actualizar uno\n2. Actualizar varios")
            update_choice = console.input("Seleccione opción (1-2): ")
            
            if update_choice == "1":
                # update_one() - Método para actualizar un documento
                try:
                    filter_query = console.input("Ingrese filtro (ej: {'nombre': 'Juan'}): ")
                    update_query = console.input("Ingrese actualización (ej: {'$set': {'edad': 25}}): ")
                    filter_dict = eval(filter_query) if filter_query else {}
                    update_dict = eval(update_query) if update_query else {}
                    
                    result = collection.update_one(filter_dict, update_dict)
                    console.print(f"\n✅[green]Documentos encontrados: {result.matched_count}[/green]")
                    console.print(f"✅[green]Documentos modificados: {result.modified_count}[/green]")
                except Exception as e:
                    console.print(f"\n❌[red]Error al actualizar: {e}[/red]")
                    
            elif update_choice == "2":
                # update_many() - Método para actualizar múltiples documentos
                try:
                    filter_query = console.input("Ingrese filtro (ej: {'activo': true}): ")
                    update_query = console.input("Ingrese actualización (ej: {'$set': {'estado': 'actualizado'}}): ")
                    filter_dict = eval(filter_query) if filter_query else {}
                    update_dict = eval(update_query) if update_query else {}
                    
                    result = collection.update_many(filter_dict, update_dict)
                    console.print(f"\n✅[green]Documentos encontrados: {result.matched_count}[/green]")
                    console.print(f"✅[green]Documentos modificados: {result.modified_count}[/green]")
                except Exception as e:
                    console.print(f"\n❌[red]Error al actualizar: {e}[/red]")
                    
        elif choice == "4":
            # Operaciones de eliminación (Delete)
            console.print("\n[bold]Eliminar documentos[/bold]")
            console.print("1. Eliminar uno\n2. Eliminar varios")
            delete_choice = console.input("Seleccione opción (1-2): ")
            
            if delete_choice == "1":
                # delete_one() - Método para eliminar un documento
                try:
                    query = console.input("Ingrese filtro (ej: {'_id': ObjectId('...')}): ")
                    query = eval(query) if query else {}
                    result = collection.delete_one(query)
                    console.print(f"\n✅[green]Documentos eliminados: {result.deleted_count}[/green]")
                except Exception as e:
                    console.print(f"\n❌[red]Error al eliminar: {e}[/red]")
                    
            elif delete_choice == "2":
                # delete_many() - Método para eliminar múltiples documentos
                try:
                    query = console.input("Ingrese filtro (ej: {'activo': false}): ")
                    query = eval(query) if query else {}
                    
                    # Confirmar eliminación múltiple
                    count = collection.count_documents(query)
                    if count > 0:
                        confirm = console.input(f"Se eliminarán {count} documentos. ¿Confirmar? (s/n): ")
                        if confirm.lower() == 's':
                            result = collection.delete_many(query)
                            console.print(f"\n✅[green]Documentos eliminados: {result.deleted_count}[/green]")
                        else:
                            console.print("\nℹ️ Operación cancelada")
                    else:
                        console.print("\nℹ️ No se encontraron documentos para eliminar")
                except Exception as e:
                    console.print(f"\n❌[red]Error al eliminar: {e}[/red]")
                    
        elif choice == "5":
            # Operaciones de conteo
            console.print("\n[bold]Contar documentos[/bold]")
            try:
                query = console.input("Ingrese filtro (opcional, ej: {'activo': true}): ")
                query = eval(query) if query else {}
                
                # count_documents() - Método para contar documentos
                count = collection.count_documents(query)
                console.print(f"\n✅[green]Total de documentos: {count}[/green]")
            except Exception as e:
                console.print(f"\n❌[red]Error al contar documentos: {e}[/red]")
                
        else:
            console.print("\n❌[red]Opción inválida. Intente nuevamente.[/red]")
        
        console.input("\nPresione Enter para continuar...")
        console.clear()