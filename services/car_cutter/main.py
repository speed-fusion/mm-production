import sys

sys.path.append("/libs")

from pulsar_manager import PulsarManager

from mongo_database import MongoDatabase

from car_cutter_api import CarCutter

class TopicHandler:
    def __init__(self):
        print("transform topic handler init")
        
        pulsar_manager = PulsarManager()
        
        self.consumer = pulsar_manager.create_consumer(pulsar_manager.topics.CAR_CUTTER)
        
        self.producer = pulsar_manager.create_producer(pulsar_manager.topics.GENERATE_IMAGE)
        
        self.mongodb = MongoDatabase()
        
        self.car_cutter = CarCutter()
    
    
    def main(self):
        print("listening for new messages")
        while True:
            
            message =  self.consumer.consume_message()
            
            website_id = message["website_id"]
            
            listing_id = message["listing_id"]
            
            where = {"_id":listing_id}
            
            data = message.get("data",None)
            
            if data == None:
                data = self.mongodb.listings_collection.find_one(where)
            
            if data == None:
                # add code to report this incident
                continue
            
            
            if website_id == 17:
                pass
            
            if website_id == 18:
                source_mrp = data["source_mrp"]
                
                if source_mrp > 10000:
                    images = [i["url"] for i in list(self.mongodb.images_collection.find({"listing_id":listing_id,"is_car_image":True,"cc_status":None}))]
                    
                    processed_images,cc_total_img = self.car_cutter.process_images(images,website_id,listing_id)
                    
                    for img in processed_images:
                        tmp = {}
                        tmp["angle"] = img["angle"]
                        tmp["path"] = img["path"]
                        tmp["cc_status"] = img["cc_status"]
                        tmp["image_ready"] = 1
                        tmp["position"] = img["position"]
                        
                        self.mongodb.images_collection.update_one({"_id":img["id"]},{"$set":tmp})
                    
                    self.mongodb.listings_collection.update_one(where,{"$set":{
                        "cc_status":1,
                        "cc_total_img":cc_total_img
                    }})
            
            self.producer.produce_message(message)


if __name__ == "__main__":
    topic_handler = TopicHandler()
    topic_handler.main()

