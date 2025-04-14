#include <iostream>
#include <libpq-fe.h>

int main() {
    // Cadena de conexión (similar a tus parámetros Python)
    const char* conninfo = "dbname=postgres user=postgres password=123456 host=localhost";
    
    // Establecer conexión
    PGconn* conn = PQconnectdb(conninfo);
    
    // Verificar conexión exitosa
    if (PQstatus(conn) != CONNECTION_OK) {
        std::cerr << "Error de conexión: " << PQerrorMessage(conn);
        PQfinish(conn);
        return 1;
    }
    
    std::cout << "✅ Conexión exitosa a PostgreSQL" << std::endl;
    
    // Cerrar conexión al finalizar
    PQfinish(conn);
    return 0;
}