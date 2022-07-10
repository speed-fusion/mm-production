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
        
        self.mc_dealers_collection = self.db["market-check-dealers"]
        
        self.valuation_data = self.db["valuation-data"]
    
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
        data["updated_at"] = get_current_datetime()
        
        if result != None:
            what = {}
            what["raw"] = data["raw"]
            what["updated_at"] = get_current_datetime()
            
            self.mc_listings_collection.update_one(where,{
                "$set":what
            })
            return result["_id"]
        
        data["created_at"] =  get_current_datetime()
        data["_id"] = generate_unique_uuid()
        data["status"] = "to_parse"
        
        self.mc_listings_collection.insert_one(data)
        
        return data["_id"]
    
    def get_active_dealer_ids(self):
        dealer_ids = {}
        
        for dealer in self.mc_dealers_collection.find({"status":"active"}):
            dealer_ids[dealer["dealer_id"]] = 1
        
        return dealer_ids
            
        