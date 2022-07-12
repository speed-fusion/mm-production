import sys

import pymongo

sys.path.append("/libs")

from pulsar_manager import PulsarManager

from mongo_database import MongoDatabase

from image_generator import ImageGenerator

class TopicHandler:
    def __init__(self):
        print("transform topic handler init")
        
        pulsar_manager = PulsarManager()
        
        self.consumer = pulsar_manager.create_consumer(pulsar_manager.topics.GENERATE_IMAGE)
        
        self.producer = pulsar_manager.create_producer(pulsar_manager.topics.FL_LISTING_PHOTOS_INSERT)
        
        self.mongodb = MongoDatabase()
        
        self.image_generator = ImageGenerator()
    
    
    def main(self):
        print("listening for new messages")
        while True:
            
            message =  self.consumer.consume_message()
            
            website_id = message["website_id"]
            
            listing_id = message["listing_id"]
            
            where = {"_id":listing_id}
            
            data = self.mongodb.listings_collection.find_one(where)
            
            if data == None:
                # add code to report this incident
                continue
            
            
            if website_id == 17:
                pass
            
            if website_id == 18:
                
                mysql_listing_id = data["mysql_listing_id"]
                
                images = list(self.mongodb.images_collection.find({"listing_id":listing_id,"is_car_image":True,"image_ready":1}).sort("position",pymongo.ASCENDING))
                
                result = self.image_generator.processListing(images,website_id,mysql_listing_id)
                
                for item in result:
                    
                    tmp = {}
                    tmp["image_generation_status"] = item["status"]
                    tmp["org"] = item["org"]
                    tmp["large"] = item["large"]
                    tmp["thumb"] = item["thumb"]
                    self.mongodb.images_collection.update_one({"_id":item["id"]},{"$set":tmp})
            
            self.producer.produce_message(message)


if __name__ == "__main__":
    topic_handler = TopicHandler()
    topic_handler.main()


     # tmp = {}
                    
                    # tmp["Listing_ID"] = mysql_listing_id
                    
                    # tmp["Position"] = item["position"]
                    
                    # tmp["Photo"] = item["large"]["path"]
                    
                    # tmp["Thumbnail"] = item["thumb"]["path"]
            
                    # tmp["Original"] = item["org"]["path"]
                    
                    # tmp["Status"] = "active"
                    
                    # tmp["Type"] = "picture"
                    
                    # tmp["create_ts"] = {"func":"now()"}
                    
                    # tmp["delete_banner_flag"] = 0
                    
                    # tmp["approved_from_dashboard"] = 1
                    
                    
                    # try:
                        
                    #     self.mysqldb.recInsert("fl_listing_photos",tmp)
                    
                    # except Exception as e:
                    #     print(f'error : {str(e)}')
                
                # self.mysqldb
                
                # self.mysqldb.disconnect()