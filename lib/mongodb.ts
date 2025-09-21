import { MongoClient, Db } from 'mongodb';

const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017/it-help-desk';
const dbName = process.env.MONGODB_DB || 'it-help-desk';

let client: MongoClient;
let db: Db;

export async function connectToDatabase() {
  if (db) {
    return db;
  }

  try {
    client = new MongoClient(uri);
    await client.connect();
    db = client.db(dbName);
    console.log('[MONGODB] Connected to database:', dbName);
    return db;
  } catch (error) {
    console.error('[MONGODB] Connection error:', error);
    throw error;
  }
}

export async function getCollection(collectionName: string) {
  const database = await connectToDatabase();
  return database.collection(collectionName);
}
