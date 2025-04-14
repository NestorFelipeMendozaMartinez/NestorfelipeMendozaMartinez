#include <iostream>
#include <mysql/mysql.h>

int main() {
    MYSQL* conn;
    conn = mysql_init(nullptr);

    // Connect to MySQL (same parameters as your Python code)
    if (!mysql_real_connect(
        conn, 
        "localhost",  // host
        "root",       // user
        "123456",    // password
        nullptr,      // database (optional)
        0,            // port (0 for default)
        nullptr,      // unix_socket (optional)
        0             // client_flag
    )) {
        std::cerr << "❌ Connection failed: " << mysql_error(conn) << std::endl;
        return 1;
    }

    std::cout << "✅ MySQL connection successful" << std::endl;

    // Clean up
    mysql_close(conn);
    return 0;
}