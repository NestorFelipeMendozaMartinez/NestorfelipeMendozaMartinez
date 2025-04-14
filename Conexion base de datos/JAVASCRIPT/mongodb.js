const { MongoClient } = require('mongodb');

async function connectMongoDB() {
  const uri = "mongodb://localhost:27017";
  const client = new MongoClient(uri);

  try {
    await client.connect();
    console.log("✅ Conexión exitosa a MongoDB");
    
    // Verificación adicional (opcional)
    const adminDb = client.db('admin');
    const serverStatus = await adminDb.command({ serverStatus: 1 });
    console.log(`Versión de MongoDB: ${serverStatus.version}`);
    
  } catch (err) {
    console.error("❌ Error de conexión:", err.message);
  } finally {
    await client.close();
  }
}

connectMongoDB();