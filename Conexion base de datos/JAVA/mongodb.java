import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoClient;

public class MongoDBConnection {
    public static void main(String[] args) {
        String connectionString = "mongodb://localhost:27017";
        
        try (MongoClient mongoClient = MongoClients.create(connectionString)) {
            System.out.println("✅ Conexión exitosa a MongoDB");
            
            // Verificación adicional (opcional)
            System.out.println("Versión del servidor: " + 
                mongoClient.getDatabase("admin")
                          .runCommand(new Document("serverStatus", 1))
                          .getString("version"));
        } catch (Exception e) {
            System.err.println("❌ Error de conexión: " + e.getMessage());
        }
    }
}