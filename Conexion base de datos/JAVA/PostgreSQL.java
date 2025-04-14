import java.sql.Connection;
import java.sql.DriverManager;

public class PostgreSQLConnection {
    public static void main(String[] args) {
        String url = "jdbc:postgresql://localhost:5432/postgres";
        String user = "postgres";
        String password = "123456";
        
        try (Connection conn = DriverManager.getConnection(url, user, password)) {
            System.out.println("✅ Conexión exitosa a PostgreSQL");
        } catch (Exception e) {
            System.err.println("❌ Error de conexión: " + e.getMessage());
        }
    }
}