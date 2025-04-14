require 'mongo'

begin
  # Conexión básica a MongoDB (sin autenticación)
  client = Mongo::Client.new('mongodb://localhost:27017')
  
  # Verificación de conexión
  client.database.command(ping: 1)
  
  puts "✅ Conexión exitosa a MongoDB"
  puts "   Versión del servidor: #{client.server_info['version']}"

rescue Mongo::Error::NoServerAvailable => e
  puts "❌ Error: No se pudo conectar a MongoDB"
  puts "   Detalle: #{e.message}"

ensure
  client&.close  # Cierra la conexión si existe
end