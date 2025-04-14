<?php
$host = "localhost";
$dbname = "postgres";
$user = "postgres";
$password = "123456";

try {
    // Cadena de conexión
    $conn = new PDO("pgsql:host=$host;dbname=$dbname", $user, $password);
    
    // Configurar el manejo de errores
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    echo "✅ Conexión exitosa a PostgreSQL";
    
} catch (PDOException $e) {
    echo "❌ Error de conexión: " . $e->getMessage();
}
?>