import pymongo
import os

user = ""
password = "9076b974c31e4678f"
host = "localhost:27017"
database = "multilingual-examples"


class Database:
    def __init__(self):
        db_name = database
        connection_uri = f'mongodb://{user}:{password}@{host}/?authSource=admin'
        # connection_uri = f'mongodb://{host}/?authSource=admin'
        
        client = pymongo.MongoClient(connection_uri)
        
        self.db = client[db_name]