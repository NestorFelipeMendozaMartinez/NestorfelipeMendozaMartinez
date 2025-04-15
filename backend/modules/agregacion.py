from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def run(db):
    console.print(Panel.fit("📊[bold cyan]Consultas y Agregaciones[/bold cyan] 📊"))
    
    with db.get_cursor() as cur:
        cur.execute("""
            SELECT categoria_id, COUNT(*) AS total, AVG(precio) AS promedio
            FROM productos
            GROUP BY categoria_id
        """)
        
        rows = cur.fetchall()
        
        table = Table(title="Resumen por Categoría")
        for col in rows[0].keys():
            table.add_column(col)
            
        for row in rows:
            table.add_row(*[str(v) for v in row.values()])
            
        console.print(table)
        