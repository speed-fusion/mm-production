import sys

sys.path.append("/libs")

from pulsar_manager import PulsarManager

from mongo_database import MongoDatabase

from calculation import MarketCheckCalculation

class TopicHandler:
    def __init__(self):
        print("transform topic handler init")
        
        pulsar_manager = PulsarManager()
        
        self.consumer = pulsar_manager.create_consumer(pulsar_manager.topics.LISTING_POST_CALCULATION)
        
        self.producer = pulsar_manager.create_producer(pulsar_manager.topics.LISTINGS_UPSERT_PROD_DB)
        
        self.mc_calculation = MarketCheckCalculation()
        
        self.mongodb = MongoDatabase()
    
    
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
                
                self.mc_calculation.update_admin_fee(data)
                
                self.mc_calculation.calculate_source_mrp(data)
                
                self.mc_calculation.calculate_margin(data)
                
                self.mc_calculation.calculate_motor_market_price(data)
                
                self.mc_calculation.calculate_pcp_apr(data)
                
                self.mc_calculation.calculate_ltv(data)
                
                self.mc_calculation.calculate_category_id(data)
                
                self.mc_calculation.car_cutter_extra_margin(data)
                
                category_id = data.get("category_id",None)
                
                if category_id == None:
                    print(f'can not generate category id for listing : {category_id}')
                    
                    what = {
                        "listing_id":listing_id,
                        "message":'can not generate category id for listing'
                    }
                    
                    self.mongodb.insert_event(self.mongodb.listing_event_collection,what)
                    
                    continue
                
                self.mongodb.listings_collection.update_one(where,{
                    "$set":data
                })
            
            self.producer.produce_message(message)  
            
        
if __name__ == "__main__":
    topic_handler = TopicHandler()
    topic_handler.main()

