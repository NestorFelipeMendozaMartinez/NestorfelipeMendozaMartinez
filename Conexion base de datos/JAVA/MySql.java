import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class MySQLSimpleConnection {
    public static void main(String[] args) {
        // Parámetros de conexión
        String url = "jdbc:mysql://localhost:3306/";
        String user = "root";
        String password = "123456";
        
        Connection conn = null;
        
        try {
            // 1. Registrar el driver (no necesario desde JDBC 4.0+)
            Class.forName("com.mysql.cj.jdbc.Driver");
            
            // 2. Establecer conexión
            conn = DriverManager.getConnection(url, user, password);
            
            // 3. Crear Statement (equivalente al cursor en Python)
            // (No se usa en este ejemplo ya que es solo para conexión)
            
            System.out.println("✅ Conexión exitosa a MySQL");
            
        } catch (ClassNotFoundException e) {
            System.err.println("Error: Driver JDBC no encontrado");
            e.printStackTrace();
        } catch (SQLException e) {
            System.err.println("❌ Error de conexión SQL: " + e.getMessage());
        } finally {
            // 4. Cerrar conexión
            if (conn != null) {
                try {
                    conn.close();
                } catch (SQLException e) {
                    System.err.println("Error al cerrar conexión: " + e.getMessage());
                }
            }
        }
    }
}