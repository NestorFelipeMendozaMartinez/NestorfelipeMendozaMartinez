require 'mysql2'

begin
  client = Mysql2::Client.new(
    host: "localhost",  # Servidor (puede ser una IP como "192.168.1.100")
    username: "root",   # Usuario de MySQL
    password: "123456"  # Contraseña
  )
  
  puts "✅ ¡Conectado a MySQL correctamente!"
  
rescue Mysql2::Error => e
  puts "❌ Error de conexión: #{e.message}"

ensure
  if client
    client.close
    puts "🔌 Conexión cerrada"
  end
end