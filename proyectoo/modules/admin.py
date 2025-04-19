from rich.console import Console  # Módulo para mejorar la presentación en consola
from rich.table import Table  # Módulo para crear tablas en consola
from rich.panel import Panel  # Módulo para crear paneles decorativos
from rich.progress import Progress  # Módulo para barras de progreso
import subprocess  # Módulo para ejecutar comandos del sistema
import os  # Módulo para operaciones del sistema operativo
from datetime import datetime  # Módulo para manejo de fechas
import time  # Módulo para operaciones con tiempo
import json  # Módulo para manejo de JSON

# Creación de una instancia de Console para la interfaz
console = Console()

def run(db):
    """
    Módulo de administración de MongoDB
    Args:
        db: Instancia de base de datos MongoDB
    Este módulo permite:
    - Ver estadísticas del servidor
    - Gestionar usuarios y roles
    - Realizar copias de seguridad
    - Importar y exportar datos
    """
    console.print(Panel.fit("⚙️[bold cyan]Administración de MongoDB[/bold cyan] ⚙️"))
    
    while True:
        # Crear tabla de menú con opciones disponibles
        table = Table(title="Operaciones de Administración", show_header=True)
        table.add_column("Opción", style="cyan")
        table.add_column("Operación", style="green")
        table.add_column("Descripción", style="white")
        
        # Agregar opciones al menú
        table.add_row("1", "Estadísticas del servidor", "Ver información del servidor MongoDB")
        table.add_row("2", "Gestión de usuarios", "Crear y administrar usuarios")
        table.add_row("3", "Gestión de roles", "Administrar roles y permisos")
        table.add_row("4", "Monitoreo de operaciones", "Ver operaciones en curso")
        table.add_row("5", "Gestión de colecciones", "Administrar colecciones")
        table.add_row("6", "Análisis de rendimiento", "Ver estadísticas de rendimiento")
        table.add_row("0", "Volver", "Regresar al menú principal")
        console.print(table)

        choice = console.input("\n🔹Seleccione una operación (0-6): ")
        
        if choice == "0":
            break
        elif choice == "1":
            # Estadísticas del servidor
            console.print("\n[bold]Estadísticas del servidor:[/bold]")
            try:
                # Obtener información del servidor
                server_info = db.command("serverStatus")
                # Obtener estadísticas de la base de datos
                db_stats = db.command("dbStats")
                
                # Tabla de información general
                info_table = Table(title="Información del Servidor", show_header=False)
                info_table.add_column("Campo")
                info_table.add_column("Valor")
                
                # Información básica
                info_table.add_row("Host", f"{db.client.HOST}:{db.client.PORT}")
                info_table.add_row("Versión MongoDB", server_info["version"])
                info_table.add_row("Motor de almacenamiento", server_info["storageEngine"]["name"])
                info_table.add_row("Tiempo de actividad", f"{server_info['uptime'] / 3600:.2f} horas")
                info_table.add_row("Base de datos actual", db.name)
                info_table.add_row("Tamaño de datos", f"{db_stats['dataSize'] / (1024*1024):.2f} MB")
                info_table.add_row("Almacenamiento usado", f"{db_stats['storageSize'] / (1024*1024):.2f} MB")
                info_table.add_row("Índices", str(db_stats["indexes"]))
                info_table.add_row("Tamaño de índices", f"{db_stats['indexSize'] / (1024*1024):.2f} MB")
                console.print(info_table)

                # Tabla de métricas de rendimiento
                perf_table = Table(title="Métricas de Rendimiento", show_header=True)
                perf_table.add_column("Métrica")
                perf_table.add_column("Valor")
                
                # Métricas de operaciones
                ops = server_info.get("opcounters", {})
                for op, count in ops.items():
                    perf_table.add_row(f"Operaciones {op}", str(count))
                
                # Métricas de conexiones
                conn = server_info.get("connections", {})
                perf_table.add_row("Conexiones actuales", str(conn.get("current", 0)))
                perf_table.add_row("Conexiones disponibles", str(conn.get("available", 0)))
                console.print(perf_table)
                
            except Exception as e:
                console.print(f"\n❌[red]Error al obtener estadísticas: {e}[/red]")
                
        elif choice == "2":
            # Gestión de usuarios
            console.print("\n[bold]Gestión de usuarios[/bold]")
            console.print("1. Listar usuarios\n2. Crear usuario\n3. Modificar roles\n4. Eliminar usuario")
            user_choice = console.input("Seleccione opción (1-4): ")
            admin_db = db.client["admin"]
            
            if user_choice == "1":
                try:
                    users = list(admin_db.command("usersInfo")["users"])
                    if users:
                        user_table = Table(title="Usuarios del Sistema", show_header=True)
                        user_table.add_column("Usuario")
                        user_table.add_column("Roles")
                        user_table.add_column("Base de datos")
                        
                        for user in users:
                            roles = ", ".join([f"{r['role']}" for r in user["roles"]])
                            dbs = ", ".join(set([r["db"] for r in user["roles"]]))
                            user_table.add_row(user["user"], roles, dbs)
                        console.print(user_table)
                    else:
                        console.print("\nℹ️ No hay usuarios definidos")
                except Exception as e:
                    console.print(f"\n❌[red]Error al listar usuarios: {e}[/red]")
                    
            elif user_choice == "2":
                try:
                    username = console.input("Nombre de usuario: ")
                    password = console.input("Contraseña: ", password=True)
                    
                    # Mostrar roles disponibles
                    roles_table = Table(title="Roles Disponibles", show_header=True)
                    roles_table.add_column("Rol")
                    roles_table.add_column("Descripción")
                    
                    available_roles = [
                        ("read", "Lectura en base de datos"),
                        ("readWrite", "Lectura y escritura"),
                        ("dbAdmin", "Administración de base de datos"),
                        ("userAdmin", "Administración de usuarios"),
                        ("clusterAdmin", "Administración del cluster"),
                        ("backup", "Operaciones de backup"),
                        ("restore", "Operaciones de restore")
                    ]
                    
                    for role, desc in available_roles:
                        roles_table.add_row(role, desc)
                    console.print(roles_table)

                    roles_input = console.input("Roles (separados por coma): ")
                    db_name = console.input("Base de datos para los roles: ")
                    
                    roles = []
                    for role in roles_input.split(","):
                        roles.append({"role": role.strip(), "db": db_name.strip()})
                    
                    admin_db.command("createUser", username, pwd=password, roles=roles)
                    console.print("\n✅[green]Usuario creado correctamente[/green]")
                    
                except Exception as e:
                    console.print(f"\n❌[red]Error al crear usuario: {e}[/red]")
                    
            elif user_choice == "3":
                try:
                    username = console.input("Nombre de usuario: ")
                    roles_input = console.input("Nuevos roles (separados por coma): ")
                    db_name = console.input("Base de datos para los roles: ")
                    
                    roles = []
                    for role in roles_input.split(","):
                        roles.append({"role": role.strip(), "db": db_name.strip()})
                    
                    admin_db.command("updateUser", username, roles=roles)
                    console.print("\n✅[green]Roles actualizados correctamente[/green]")
                    
                except Exception as e:
                    console.print(f"\n❌[red]Error al modificar roles: {e}[/red]")
                    
            elif user_choice == "4":
                try:
                    username = console.input("Nombre de usuario a eliminar: ")
                    confirm = console.input(f"¿Está seguro de eliminar al usuario '{username}'? (s/n): ")
                    
                    if confirm.lower() == "s":
                        admin_db.command("dropUser", username)
                        console.print("\n✅[green]Usuario eliminado correctamente[/green]")
                    else:
                        console.print("\nℹ️ Operación cancelada")
                        
                except Exception as e:
                    console.print(f"\n❌[red]Error al eliminar usuario: {e}[/red]")
                    
        elif choice == "3":
            # Gestión de roles
            console.print("\n[bold]Gestión de roles[/bold]")
            console.print("1. Listar roles\n2. Crear rol\n3. Modificar privilegios\n4. Eliminar rol")
            role_choice = console.input("Seleccione opción (1-4): ")
            
            if role_choice == "1":
                try:
                    roles = list(admin_db.command("rolesInfo")["roles"])
                    if roles:
                        role_table = Table(title="Roles del Sistema", show_header=True)
                        role_table.add_column("Rol")
                        role_table.add_column("Base de datos")
                        role_table.add_column("Privilegios")
                        
                        for role in roles:
                            privs = ", ".join([f"{p['resource']['db']}.{p['resource'].get('collection', '*')}" 
                                            for p in role.get("privileges", [])])
                            role_table.add_row(role["role"], role["db"], privs)
                        console.print(role_table)
                    else:
                        console.print("\nℹ️ No hay roles personalizados definidos")
                except Exception as e:
                    console.print(f"\n❌[red]Error al listar roles: {e}[/red]")
                    
        elif choice == "4":
            # Monitoreo de operaciones
            console.print("\n[bold]Operaciones en curso:[/bold]")
            try:
                current_ops = db.current_op()["inprog"]
                if current_ops:
                    ops_table = Table(title="Operaciones Activas", show_header=True)
                    ops_table.add_column("ID")
                    ops_table.add_column("Tipo")
                    ops_table.add_column("Namespace")
                    ops_table.add_column("Duración (ms)")
                    ops_table.add_column("Estado")
                    
                    for op in current_ops:
                        ops_table.add_row(
                            str(op.get("opid", "N/A")),
                            op.get("op", "N/A"),
                            op.get("ns", "N/A"),
                            str(op.get("microsecs_running", 0) // 1000),
                            op.get("state", "N/A")
                        )
                    console.print(ops_table)
                else:
                    console.print("\nℹ️ No hay operaciones activas")
            except Exception as e:
                console.print(f"\n❌[red]Error al obtener operaciones: {e}[/red]")
                
        elif choice == "5":
            # Gestión de colecciones
            console.print("\n[bold]Gestión de colecciones[/bold]")
            console.print("1. Listar colecciones\n2. Crear colección\n3. Eliminar colección\n4. Estadísticas")
            col_choice = console.input("Seleccione opción (1-4): ")
            
            if col_choice == "1":
                try:
                    collections = db.list_collection_names()
                    if collections:
                        col_table = Table(title="Colecciones en la Base de Datos", show_header=True)
                        col_table.add_column("Nombre")
                        col_table.add_column("Documentos")
                        col_table.add_column("Tamaño")
                        col_table.add_column("Índices")
                        
                        for col_name in collections:
                            stats = db.command("collstats", col_name)
                            col_table.add_row(
                                col_name,
                                str(stats["count"]),
                                f"{stats['size'] / (1024*1024):.2f} MB",
                                str(len(stats["indexSizes"]))
                            )
                        console.print(col_table)
                    else:
                        console.print("\nℹ️ No hay colecciones en la base de datos")
                except Exception as e:
                    console.print(f"\n❌[red]Error al listar colecciones: {e}[/red]")
                    
            elif col_choice == "2":
                try:
                    name = console.input("Nombre de la nueva colección: ")
                    capped = console.input("¿Colección limitada? (s/n) [n]: ").lower() == "s"
                    options = {}
                    
                    if capped:
                        size = int(console.input("Tamaño máximo (bytes): "))
                        max_docs = console.input("Número máximo de documentos (opcional): ")
                        options["capped"] = True
                        options["size"] = size
                        if max_docs:
                            options["max"] = int(max_docs)
                    
                    db.create_collection(name, **options)
                    console.print("\n✅[green]Colección creada correctamente[/green]")
                except Exception as e:
                    console.print(f"\n❌[red]Error al crear colección: {e}[/red]")
                    
            elif col_choice == "3":
                try:
                    collections = db.list_collection_names()
                    if not collections:
                        console.print("\nℹ️ No hay colecciones para eliminar")
                        continue
                    
                    console.print("\nColecciones disponibles:")
                    for i, name in enumerate(collections, 1):
                        console.print(f"{i}. {name}")
                    
                    col_index = int(console.input("\nSeleccione colección a eliminar (número): ")) - 1
                    
                    if 0 <= col_index < len(collections):
                        col_name = collections[col_index]
                        confirm = console.input(f"¿Está seguro de eliminar la colección '{col_name}'? (s/n): ")
                        
                        if confirm.lower() == "s":
                            db[col_name].drop()
                            console.print("\n✅[green]Colección eliminada correctamente[/green]")
                        else:
                            console.print("\nℹ️ Operación cancelada")
                    else:
                        console.print("\n❌[red]Opción inválida[/red]")
                except Exception as e:
                    console.print(f"\n❌[red]Error al eliminar colección: {e}[/red]")
                    
            elif col_choice == "4":
                try:
                    collections = db.list_collection_names()
                    if not collections:
                        console.print("\nℹ️ No hay colecciones para analizar")
                        continue
                    
                    console.print("\nColecciones disponibles:")
                    for i, name in enumerate(collections, 1):
                        console.print(f"{i}. {name}")
                    
                    col_index = int(console.input("\nSeleccione colección (número): ")) - 1
                    
                    if 0 <= col_index < len(collections):
                        col_name = collections[col_index]
                        stats = db.command("collstats", col_name)
                        
                        stats_table = Table(title=f"Estadísticas de '{col_name}'", show_header=False)
                        stats_table.add_column("Métrica")
                        stats_table.add_column("Valor")
                        
                        metrics = [
                            ("Documentos", stats["count"]),
                            ("Tamaño de datos", f"{stats['size'] / (1024*1024):.2f} MB"),
                            ("Tamaño en disco", f"{stats['storageSize'] / (1024*1024):.2f} MB"),
                            ("Número de índices", len(stats["indexSizes"])),
                            ("Tamaño de índices", f"{stats['totalIndexSize'] / (1024*1024):.2f} MB"),
                            ("Colección limitada", "Sí" if stats.get("capped", False) else "No")
                        ]
                        
                        for metric, value in metrics:
                            stats_table.add_row(metric, str(value))
                        console.print(stats_table)
                        
                        # Mostrar información de índices
                        if stats["indexSizes"]:
                            idx_table = Table(title="Índices", show_header=True)
                            idx_table.add_column("Nombre")
                            idx_table.add_column("Tamaño")
                            
                            for idx_name, idx_size in stats["indexSizes"].items():
                                idx_table.add_row(
                                    idx_name,
                                    f"{idx_size / (1024*1024):.2f} MB"
                                )
                            console.print(idx_table)
                    else:
                        console.print("\n❌[red]Opción inválida[/red]")
                except Exception as e:
                    console.print(f"\n❌[red]Error al obtener estadísticas: {e}[/red]")
                    
        elif choice == "6":
            # Análisis de rendimiento
            console.print("\n[bold]Análisis de rendimiento[/bold]")
            try:
                # Obtener estadísticas del servidor
                server_status = db.command("serverStatus")
                
                # Métricas de operaciones
                ops_table = Table(title="Operaciones por Segundo", show_header=True)
                ops_table.add_column("Tipo")
                ops_table.add_column("Total")
                ops_table.add_column("Por segundo")
                
                start_ops = server_status["opcounters"]
                time.sleep(1)  # Esperar 1 segundo
                end_ops = db.command("serverStatus")["opcounters"]
                
                for op in start_ops:
                    total = start_ops[op]
                    per_second = end_ops[op] - start_ops[op]
                    ops_table.add_row(op, str(total), str(per_second))
                console.print(ops_table)
                
                # Métricas de memoria
                mem = server_status.get("mem", {})
                mem_table = Table(title="Uso de Memoria", show_header=False)
                mem_table.add_column("Métrica")
                mem_table.add_column("Valor")
                
                mem_metrics = [
                    ("Memoria virtual", f"{mem.get('virtual', 0) / (1024*1024):.2f} MB"),
                    ("Memoria residente", f"{mem.get('resident', 0) / (1024*1024):.2f} MB"),
                    ("Memoria mapeada", f"{mem.get('mapped', 0) / (1024*1024):.2f} MB")
                ]
                
                for metric, value in mem_metrics:
                    mem_table.add_row(metric, value)
                console.print(mem_table)
                
                # Métricas de conexiones
                conn = server_status.get("connections", {})
                conn_table = Table(title="Conexiones", show_header=False)
                conn_table.add_column("Métrica")
                conn_table.add_column("Valor")
                
                conn_metrics = [
                    ("Conexiones actuales", str(conn.get("current", 0))),
                    ("Conexiones disponibles", str(conn.get("available", 0))),
                    ("Conexiones totales", str(conn.get("totalCreated", 0)))
                ]
                
                for metric, value in conn_metrics:
                    conn_table.add_row(metric, value)
                console.print(conn_table)
                
            except Exception as e:
                console.print(f"\n❌[red]Error al analizar rendimiento: {e}[/red]")
                
        else:
            console.print("\n❌[red]Opción inválida. Intente nuevamente.[/red]")
        
        console.input("\nPresione Enter para continuar...")
        console.clear()