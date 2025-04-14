
const mysql = require('mysql2/promise');  

async function connectMySQL() {
    let connection;
    
    try {
        
        connection = await mysql.createConnection({
            host: 'localhost',
            user: 'root',
            password: '123456'
        });

        console.log('✅ Conexión exitosa a MySQL');

        const [rows, fields] = await connection.execute('SHOW DATABASES');
        console.log('Bases de datos disponibles:', rows.map(row => row.Database));

    } catch (err) {
        console.error('❌ Error de conexión:', err.message);
    } finally {
        
        if (connection) await connection.end(); 
    }
}

connectMySQL();