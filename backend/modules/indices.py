from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def run(db):
    console.print(Panel.fit("📌[bold cyan]Gestión de Índices[/bold cyan] 📌"))
    
    with db.get_cursor() as cur:
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_productos_precio ON productos(precio);
        """)
        db.conn.commit()
        
        cur.execute("SELECT * FROM pg_indexes WHERE tablename = 'productos'")
        rows = cur.fetchall()
        
        table = Table(title="Índices de productos")
        for col in rows[0].keys():
            table.add_column(col)
            
        for row in rows:
            table.add_row(*[str(v) for v in row.values()])
            
        console.print(table)