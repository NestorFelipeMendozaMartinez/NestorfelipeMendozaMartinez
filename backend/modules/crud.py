from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def run(db):
    console.print(Panel.fit("🔧[bold cyan]Módulo CRUD Básico[/bold cyan] 🔧"))
    
    with db.get_cursor() as cur:
        # Insertar categoría
        cur.execute("""
            INSERT INTO categorias (nombre, descripcion) VALUES
            ('Libros', 'Categoría de libros')
            ON CONFLICT DO NOTHING;
        """)
        
        # Insertar producto
        cur.execute("""
            INSERT INTO productos (nombre, precio, categoria_id, stock, descripcion) VALUES
            ('Libro Python', 39000, 1, 25, 'Guía práctica de Python')
            ON CONFLICT DO NOTHING;
        """)
        
        db.conn.commit()
        
        # Mostrar resultados
        cur.execute("SELECT * FROM productos")
        rows = cur.fetchall()
        
        table = Table(title="Productos")
        for col in rows[0].keys():
            table.add_column(col)
            
        for row in rows:
            table.add_row(*[str(v) for v in row.values()])
            
        console.print(table)