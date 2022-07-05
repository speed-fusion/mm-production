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
        self.mc_listings_collection = self.db["market-check-listings"]
        self.mc_dealers_collection = self.db["market-check-dealers"]
    
    def upsert_dealer_mc(self,data):
        for key in data.copy():
            if data[key] == None:
                del data[key]
        
        dealer_id = data["dealer_id"]
        where = {"dealer_id":dealer_id}
        result = self.mc_dealers_collection.find_one(where)
        data["updated_at"] = get_current_datetime()
        if result != None:
            what = data
            self.mc_dealers_collection.update_one(where,{
                "$set":what
            })
            return
        
        data["created_at"] =  get_current_datetime()
        data["_id"] = generate_unique_uuid()
        data["status"] = "inactive"
        self.mc_dealers_collection.insert_one(data)
    
    def upsert_listings_mc(self,data):
        for key in data.copy():
            if data[key] == None:
                del data[key]
        
        source_id = data["source_id"]
        where = {"source_id":source_id}
        result = self.mc_listings_collection.find_one(where)
        data = {"raw":data}
        data["updated_at"] = get_current_datetime()
        
        if result != None:
            what = {
                "raw":data
            }
            
            self.mc_listings_collection.update_one(where,{
                "$set":what
            })
            return
        
        data["created_at"] =  get_current_datetime()
        data["_id"] = generate_unique_uuid()
        data["status"] = "to_parse"
        data["source_id"] = source_id
        self.mc_listings_collection.insert_one(data)
        