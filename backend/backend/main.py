from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from database import DatabaseConnection
from modules import crud, agregacion, indices, estadisticas, tutorial

console = Console()

def show_menu():
    console.print(Panel.fit("📚[bold cyan]Tutorial PostgreSQL con Python[/bold cyan] 📚"))
    menu = Table(title="Módulos Disponibles", show_header=True, header_style="bold magenta")
    menu.add_column("Opción", style="cyan")
    menu.add_column("Operación", style="green")
    menu.add_column("Descripción", style="white")
    menu.add_row("1", "Tutorial SQL", "Aprende SQL paso a paso")
    menu.add_row("2", "CRUD Básico", "Operaciones básicas de datos")
    menu.add_row("3", "Agregaciones", "Consultas y análisis de datos")
    menu.add_row("4", "Índices", "Gestión de índices")
    menu.add_row("5", "Estadísticas", "Estadísticas del sistema")
    menu.add_row("0", "Salir", "Terminar el programa")
    console.print(menu)

def main():
    try:
        db = DatabaseConnection.get_instance()
        console.print("[green]✓ Conexión exitosa a PostgreSQL[/green]")
        
        modules = {
            "1": tutorial.run,
            "2": crud.run,
            "3": agregacion.run,
            "4": indices.run,
            "5": estadisticas.run
        }
        
        while True:
            show_menu()
            choice = console.input("\n[cyan]Seleccione una opción (0-5): [/cyan]")
            
            if choice == "0":
                console.print("\n[yellow]¡Hasta luego![/yellow]")
                break
                
            if choice in modules:
                modules[choice](db)
            else:
                console.print("\n[red]Opción inválida. Intente nuevamente.[/red]")
                
    except Exception as e:
        console.print(f"[red]Error de conexión: {e}[/red]")
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    main()