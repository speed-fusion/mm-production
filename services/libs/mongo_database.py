import pymongo
import os
from datetime import datetime

from helper import generate_unique_uuid,get_current_datetime

class MongoDatabase:
    def __init__(self):
        self.user = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
        self.password = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
        self.host = "mongodb:27017"
        self.database = "motor_market"
        connection_uri = f'mongodb://{self.user}:{self.password}@{self.host}/?authSource=admin'
        client = pymongo.MongoClient(connection_uri)
        self.db = client[self.database]
        
        # market check
        self.listings_collection = self.db["listings"]
        
        self.dealers_collection = self.db["dealers"]
        
        self.valuation_data = self.db["valuation-data"]