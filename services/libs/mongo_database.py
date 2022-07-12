import pymongo
from helper import get_current_datetime
import mm_constants

class MongoDatabase:
    def __init__(self):
        self.user = mm_constants.MONGO_USERNAME
        self.password = mm_constants.MONGO_PASSWORD
        self.host = mm_constants.MONGO_HOST
        self.database = mm_constants.MONGO_DATABASE
        connection_uri = f'mongodb://{self.user}:{self.password}@{self.host}/?authSource=admin'
        client = pymongo.MongoClient(connection_uri)
        self.db = client[self.database]
        
        # market check
        self.listings_collection = self.db["listings"]
        
        self.dealers_collection = self.db["dealers"]
        
        self.images_collection = self.db["images"]
        
        self.valuation_data = self.db["valuation-data"]
        
        self.listing_event_collection = self.db["listing-events"]
    
    def insert_event(self,collection,data):
        now = get_current_datetime()
        
        data["created_at"] = now
        
        collection.insert_one(data)
    
        