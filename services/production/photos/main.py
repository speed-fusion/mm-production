import sys

sys.path.append("/libs")

from pulsar_manager import PulsarManager
import pymongo
from mongo_database import MongoDatabase
from mysql_database import MysqlDatabase

class TopicHandler:
    def __init__(self):
        print("transform topic handler init")
        
        pulsar_manager = PulsarManager()
        
        self.consumer = pulsar_manager.create_consumer(pulsar_manager.topics.FL_LISTING_PHOTOS_INSERT)
        
        self.mongodb = MongoDatabase()
        
        self.mysqldb = MysqlDatabase()
    
    
    def main(self):
        print("listening for new messages")
        while True:
            
            message =  self.consumer.consume_message()
            
            website_id = message["website_id"]
            
            listing_id = message["listing_id"]
            
            where = {"_id":listing_id}
            
            data = self.mongodb.listings_collection.find_one(where,{"raw":0})
            
            if data == None:
                # add code to report this incident
                continue
            
            
            if website_id == 17:
                pass
            
            
            if website_id == 18:
                mysql_listing_id = data["mysql_listing_id"]
                images = list(self.mongodb.images_collection.find({"listing_id":listing_id,"is_car_image":True,"image_ready":1,"mysql_photo_id":None}).sort("position",pymongo.ASCENDING))
                
                if len(images) == 0:
                    continue
                
                thumb_image_path = images[0]["thumb"]["path"]
                
                self.mysqldb.connect()
                
                self.mysqldb.recCustomQuery(f'UPDATE fl_listings SET Main_photo="{thumb_image_path}",Status="active" WHERE ID={mysql_listing_id} AND Status NOT IN("manual_expire","pending")')
                
                for item in images:
                    tmp = {}
                    
                    tmp["Listing_ID"] = mysql_listing_id
                    
                    tmp["Position"] = item["position"]
                    
                    tmp["Photo"] = item["large"]["path"]
                    
                    tmp["Thumbnail"] = item["thumb"]["path"]
            
                    tmp["Original"] = item["org"]["path"]
                    
                    tmp["Status"] = "active"
                    
                    tmp["Type"] = "picture"
                    
                    tmp["create_ts"] = {"func":"now()"}
                    
                    tmp["delete_banner_flag"] = 0
                    
                    tmp["approved_from_dashboard"] = 1
                    
                    
                    try:
                        
                        id = self.mysqldb.recInsert("fl_listing_photos",tmp)
                        
                        self.mongodb.images_collection.update_one({"_id":item["_id"]},{
                            "$set":{
                                "mysql_photo_id":id
                            }
                        })
                        
                    except Exception as e:
                        print(f'error : {str(e)}')
                
                self.mysqldb.disconnect()
        
if __name__ == "__main__":
    topic_handler = TopicHandler()
    topic_handler.main()

