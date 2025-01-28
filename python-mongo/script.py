import pymongo
import json

# Load JSON data from file
with open('python-mongo/products.json') as f:
    products = json.load(f)

with open('python-mongo/category.json') as f:
    category = json.load(f)

with open('python-mongo/users.json') as f:
    users = json.load(f)

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')

# Create a new database and collection
db = client['db2008']
productCollection = db['products']
categoryCollection = db['category']
usersCollection = db['users']

# Insert the data into the collection
productCollection.insert_many(products)
categoryCollection.insert_many(category)
usersCollection.insert_many(users)