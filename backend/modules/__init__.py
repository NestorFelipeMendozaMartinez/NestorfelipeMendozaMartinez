# modules/__init__.py
"""
Paquete que contiene todos los módulos para el tutorial de PostgreSQL:
- CRUD básico
- Operaciones de agregación
- Gestión de índices
- Estadísticas del sistema
- Tutorial SQL
"""

# Importaciones explícitas para facilitar el acceso desde otros módulos
from . import crud
from . import agregacion
from . import indices
from . import estadisticas
from . import tutorial

__all__ = ['crud', 'agregacion', 'indices', 'estadisticas', 'tutorial']