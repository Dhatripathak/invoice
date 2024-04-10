from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Access a database
db = client['mydatabase']

# Access a collection
collection = db['mycollection']

# Insert a document
result = collection.insert_one({'name': 'John', 'age': 30})
print(result.inserted_id)
