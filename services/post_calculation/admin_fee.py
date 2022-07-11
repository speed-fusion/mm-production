import sys

sys.path.append("/libs")

from mm_constants import MarketCheckConstants
from mongo_database import MongoDatabase

class MarketCheckAdminFee:
    def __init__(self) -> None:
        
        self.mongo_db = MongoDatabase()
    
    def get_admin_fee(self,dealer_id):
        admin_fee = 0
        
        where = {"dealer_id":dealer_id,"website_id":MarketCheckConstants.WEBSITE_ID.value}
        
        admin_fee_data = self.mongo_db.dealers_collection.find_one(where,{"admin_fee":1})
        
        if admin_fee_data != None:
            admin_fee = admin_fee_data["admin_fee"]
        
        return admin_fee