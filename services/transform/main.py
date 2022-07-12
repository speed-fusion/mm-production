import sys

sys.path.append("/libs")

from pulsar_manager import PulsarManager

from mongo_database import MongoDatabase

from transform import MarketCheckTransform

class TopicHandler:
    def __init__(self):
        print("transform topic handler init")
        
        pulsar_manager = PulsarManager()
        
        self.consumer = pulsar_manager.create_consumer(pulsar_manager.topics.LISTING_TRANSFORM)
        
        self.producer = pulsar_manager.create_producer(pulsar_manager.topics.LISTING_PRE_VALIDATION)
        
        self.mc_transform = MarketCheckTransform()
        
        self.at_transform = None
        
        self.mongodb = MongoDatabase()
    
    
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
            
            try:
            
                if website_id == 18:
                    final = self.mc_transform.transform(data,listing_id)
                    self.mongodb.listings_collection.update_one(
                        where,
                        {
                            "$set":final
                        }
                    )
            except Exception as e:
                print(f'error : {str(e)}')
                continue
            
            self.producer.produce_message({
            "website_id":website_id,
            "listing_id":listing_id
            })
        
if __name__ == "__main__":
    topic_handler = TopicHandler()
    topic_handler.main()

