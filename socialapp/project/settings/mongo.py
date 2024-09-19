from pymongo import MongoClient

# MongoDB Connection Parameters
MONGO_DB_URL = 'mongodb://localhost:27017'

# Create a MongoClient to the Mongo Instance
client = MongoClient(MONGO_DB_URL)

# Select the database to be used
DB = client['socialapp-db']
