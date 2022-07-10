import sys

sys.path.append("/libs")

from pulsar_manager import PulsarManager

from mongo_database import MongoDatabase

from predictor import RegistrationPredictor

class TopicHandler:
    def __init__(self):
        print("transform topic handler init")
        
        pulsar_manager = PulsarManager()
        
        self.consumer = pulsar_manager.create_consumer(pulsar_manager.topics.LISTING_PREDICT_NUMBERPLATE)
        
        self.producer = pulsar_manager.create_producer(pulsar_manager.topics.LISTING_POST_CALCULATION)
        
        self.predictor = RegistrationPredictor()
        
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
                
                images = data["downloaded_images"]
                
                registration = data["registration"]
                
                pred_data = self.predictor.predict(images,None)
                
                pred_data["registration_prediction"] = True
                
                self.mongodb.listings_collection.update_one(
                    where,
                    {
                        "$set":pred_data
                    }
                )
            
            self.producer.produce_message(message)
            
        
if __name__ == "__main__":
    topic_handler = TopicHandler()
    topic_handler.main()

