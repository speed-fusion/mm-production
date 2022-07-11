import sys

sys.path.append("/libs")

from pulsar_manager import PulsarManager

from mongo_database import MongoDatabase

from predictor import Predictor

class TopicHandler:
    def __init__(self):
        print("transform topic handler init")
        
        pulsar_manager = PulsarManager()
        
        self.consumer = pulsar_manager.create_consumer(pulsar_manager.topics.LISTING_PREDICT_MAKE_MODEL)
        
        self.producer = pulsar_manager.create_producer(pulsar_manager.topics.LISTING_PREDICT_CAR_IMAGE)
        
        self.mongodb = MongoDatabase()
        
        self.predictor = Predictor()
    
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
                
                make_model_prediction = data.get("make_model_prediction",False)
                
                if make_model_prediction == False:
                    title = data["title"]
                    
                    pred_data = self.predictor.predict(title)
                    
                    pred_data["make_model_prediction"] = True
                    
                    print(pred_data)
                    
                    self.mongodb.listings_collection.update_one(
                        where,
                        {
                            "$set":pred_data
                        }
                    )
                    
                    data.update(pred_data)
                    
                    message["data"] = data
            
            self.producer.produce_message(message)
            
        
if __name__ == "__main__":
    topic_handler = TopicHandler()
    topic_handler.main()

