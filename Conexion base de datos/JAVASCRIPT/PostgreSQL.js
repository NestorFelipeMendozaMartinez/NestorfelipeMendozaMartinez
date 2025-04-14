// Importar el cliente PostgreSQL
const { Client } = require('pg');

// Configuración de conexión (similar a tu ejemplo Python)
const client = new Client({
  host: 'localhost',
  user: 'postgres',
  password: '123456',
  database: 'postgres',
  port: 5432 // El puerto por defecto de PostgreSQL
});

// Conectar y manejar errores
client.connect()
  .then(() => {
    console.log('✅ Conexión exitosa a PostgreSQL');
    
    // Opcional: Verificar versión del servidor (como ejemplo)
    return client.query('SELECT version()');
  })
  .then(result => {
    console.log('Versión de PostgreSQL:', result.rows[0].version);
  })
  .catch(err => {
    console.error('❌ Error de conexión:', err.message);
  })
  .finally(() => {
    client.end(); // Cerrar la conexión
  });

