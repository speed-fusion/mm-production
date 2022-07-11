import sys

sys.path.append("/libs")

from pulsar_manager import PulsarManager

from mongo_database import MongoDatabase

from validation import MarketCheckValidation

class TopicHandler:
    def __init__(self):
        print("transform topic handler init")
        
        pulsar_manager = PulsarManager()
        
        self.consumer = pulsar_manager.create_consumer(pulsar_manager.topics.LISTING_PRE_VALIDATION)
        
        self.producer = pulsar_manager.create_producer(pulsar_manager.topics.LISTING_PREDICT_MAKE_MODEL)
        
        self.mc_validation = MarketCheckValidation()
        
        self.mongodb = MongoDatabase()
    
    
    def main(self):
        print("listening for new messages")
        while True:
            
            message =  self.consumer.consume_message()
            
            print(message)
            
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
                
                status,error = self.mc_validation.validate(data)
                
                if status == False:
                    
                    event_data = {
                        "listing_id":listing_id,
                        "message":error,
                        "website_id":website_id
                    }
                    
                    self.mongodb.insert_event(event_data)
                    
                    continue
            
            self.producer.produce_message(message)
            
        
if __name__ == "__main__":
    topic_handler = TopicHandler()
    topic_handler.main()

