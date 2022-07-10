from datetime import datetime
import sys

sys.path.append("/libs")

from pulsar_manager import PulsarManager

from market_check import MarketCheck


class TopicHandler:
    def __init__(self):
        
        pulsar_manager = PulsarManager()
        
        self.topics = pulsar_manager.topics
        
        self.producer = pulsar_manager.create_producer(pulsar_manager.topics.LISTING_TRANSFORM)
        
        self.marketcheck = MarketCheck()
        
    def main(self):
        
        status,listings,dealers = self.marketcheck.main()
        
        if status == False:
            return
        
        t1 = datetime.now()
        self.marketcheck.upsert_dealers(dealers)
        listings = self.marketcheck.upsert_listings(listings)
        t2 = datetime.now()
        
        print(f'total time : {(t2 - t1).seconds}')
        
        for item in listings:
            listing_id = item["listing_id"]
            
            print(f'sending message : {listing_id}')
            
            self.producer.produce_message({
                "listing_id":listing_id,
                "website_id":18,
                "data":item["data"]
            })

if __name__ == "__main__":
    topic_handler = TopicHandler()
    topic_handler.main()