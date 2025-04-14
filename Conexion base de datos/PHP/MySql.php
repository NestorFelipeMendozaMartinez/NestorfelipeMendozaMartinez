<?php
$host = "localhost";
$user = "root";
$password = "123456";

try {
    // Crear conexión
    $conn = new mysqli($host, $user, $password);
    
    // Verificar conexión
    if ($conn->connect_error) {
        throw new Exception("Error de conexión: " . $conn->connect_error);
    }
    
    echo "✅ Conexión exitosa a MySQL";
    
    // Crear cursor (equivalente al cursor de Python)
    $cursor = $conn->query("SELECT 1");
    
    // Ejemplo de consulta
    $result = $conn->query("SELECT VERSION()");
    $row = $result->fetch_row();
    echo "Versión de MySQL: " . $row[0];
    
} catch (Exception $e) {
    echo "❌ Error: " . $e->getMessage();
} finally {
    // Cerrar conexión
    if (isset($conn)) {
        $conn->close();
    }
}
?>