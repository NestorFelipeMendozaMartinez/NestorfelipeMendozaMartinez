package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/lib/pq" // Driver PostgreSQL
)

func main() {
	// Configuración de conexión (similar a tu ejemplo Python)
	connStr := "user=postgres password=123456 dbname=postgres host=localhost sslmode=disable"

	// Abrir conexión
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close() // Cerrar conexión al final

	// Verificar conexión
	err = db.Ping()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("✅ Conexión exitosa a PostgreSQL")
}