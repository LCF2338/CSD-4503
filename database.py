# database.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

# Load environment variables (ensure dotenv is loaded if necessary)
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
uri = os.getenv("MONGODB_URI")

# Initialize MongoDB client and database
client = MongoClient(f"mongodb+srv://{username}:{password}@{uri}?retryWrites=true&w=majority&appName=Cluster0")
db = client.get_database('shop_db')
