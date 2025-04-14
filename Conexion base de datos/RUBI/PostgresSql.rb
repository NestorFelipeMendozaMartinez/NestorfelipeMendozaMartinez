require 'pg'

begin
  # Establecer conexión
  conn = PG.connect(
    dbname: 'postgres',
    user: 'postgres',
    password: '123456',
    host: 'localhost'
  )
  
  puts "✅ Conexión exitosa a PostgreSQL!"
  puts "   Versión del servidor: #{conn.server_version}"

rescue PG::Error => e
  puts "❌ Error de conexión: #{e.message}"

ensure
  conn&.close
end