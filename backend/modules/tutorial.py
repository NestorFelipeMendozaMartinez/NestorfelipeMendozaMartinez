from rich.console import Console
from rich.panel import Panel

console = Console()

def run(db):
    console.print(Panel.fit("📘[bold cyan]Tutorial SQL: Comandos DDL y DML[/bold cyan] 📘"))
    
    with db.get_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100),
                descripcion TEXT
            );
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100),
                precio DECIMAL(10,2),
                categoria_id INTEGER REFERENCES categorias(id),
                stock INTEGER,
                descripcion TEXT
            );
        """)
        
        db.conn.commit()
        console.print("[green]✓ Tablas creadas correctamente[/green]")