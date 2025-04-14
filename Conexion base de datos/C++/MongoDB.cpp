#include <mongocxx/client.hpp>
#include <mongocxx/instance.hpp>
#include <iostream>

int main() {
    mongocxx::instance inst{}; // Requerido una vez por programa
    mongocxx::client client{mongocxx::uri{"mongodb://localhost:27017"}};
    std::cout << "✅ Conexión exitosa a MongoDB" << std::endl;
    return 0;
}