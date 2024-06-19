from pymongo import MongoClient
from flask_bcrypt import Bcrypt

# Initialize Bcrypt
bcrypt = Bcrypt()

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.email_app

# Function to migrate user data
def migrate_user_data():
    users = db.users.find({})
    for user in users:
        # Check if password field is missing or named incorrectly
        if 'password_hash' in user:
            hashed_password = user['password_hash']
            db.users.update_one({'_id': user['_id']}, {'$set': {'password': hashed_password}})
            db.users.update_one({'_id': user['_id']}, {'$unset': {'password_hash': ""}})
        elif 'password' not in user:
            # If password field is missing, handle appropriately (e.g., set a default password or skip)
            print(f"User {user['_id']} does not have a password field. Skipping.")

# Run migration
migrate_user_data()
print("Migration completed.")
