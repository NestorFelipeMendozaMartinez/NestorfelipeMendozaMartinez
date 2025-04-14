<?php
try {
    // Conexión básica a MongoDB
    $client = new MongoDB\Driver\Manager("mongodb://localhost:27017");
    
    // Comando para verificar la conexión (ping)
    $command = new MongoDB\Driver\Command(['ping' => 1]);
    $client->executeCommand('admin', $command);
    
    echo "✅ Conexión exitosa a MongoDB";
    
} catch (MongoDB\Driver\Exception\Exception $e) {
    echo "❌ Error de conexión: " . $e->getMessage();
}
?>