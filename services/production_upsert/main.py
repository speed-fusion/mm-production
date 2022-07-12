import sys

sys.path.append("/libs")

from pulsar_manager import PulsarManager

from mongo_database import MongoDatabase

from mapping import MarketCheckFieldMaper
class TopicHandler:
    def __init__(self):
        print("transform topic handler init")
        
        pulsar_manager = PulsarManager()
        
        self.consumer = pulsar_manager.create_consumer(pulsar_manager.topics.LISTINGS_UPSERT_PROD_DB)
        
        self.producer = pulsar_manager.create_producer(pulsar_manager.topics.GENERATE_IMAGE)
        
        self.mongodb = MongoDatabase()
        
        self.mc_mapper = MarketCheckFieldMaper()
    
    
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
                mapped_data = self.mc_mapper.map(data)
                
                self.mongodb.listings_collection.update_one(where,{
                    "$set":{
                    "mapped_data":mapped_data
                }
                })
                
            self.producer.produce_message(message)  
            
        
if __name__ == "__main__":
    topic_handler = TopicHandler()
    topic_handler.main()

