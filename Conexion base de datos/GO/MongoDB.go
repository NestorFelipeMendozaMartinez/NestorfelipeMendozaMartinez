package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func main() {
	// Configuración de conexión
	clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")
	
	// Conectar con timeout de 10 segundos
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	
	client, err := mongo.Connect(ctx, clientOptions)
	if err != nil {
		log.Fatal(err)
	}
	
	// Verificar conexión
	err = client.Ping(ctx, nil)
	if err != nil {
		log.Fatal(err)
	}
	
	fmt.Println("✅ Conexión exitosa a MongoDB")
	
	// Cerrar conexión cuando termine
	defer func() {
		if err = client.Disconnect(ctx); err != nil {
			log.Fatal(err)
		}
	}()
}