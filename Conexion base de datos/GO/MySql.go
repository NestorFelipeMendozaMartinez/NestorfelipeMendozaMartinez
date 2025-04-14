package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/go-sql-driver/mysql" // Driver MySQL
)

func main() {
	// Configuración de conexión (similar a tu ejemplo Python)
	dsn := "root:123456@tcp(localhost:3306)/" // Formato: usuario:contraseña@protocolo(host:puerto)/basedatos

	// Abrir conexión
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		log.Fatal("Error al abrir conexión:", err)
	}
	defer db.Close() // Importante: cerrar conexión al final

	// Verificar conexión
	err = db.Ping()
	if err != nil {
		log.Fatal("Error al conectar:", err)
	}

	fmt.Println("✅ Conexión exitosa a MySQL")
}