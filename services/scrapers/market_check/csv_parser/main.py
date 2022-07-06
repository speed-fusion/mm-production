from datetime import datetime
import sys

sys.path.append("/libs")

from pulsar_manager import PulsarManager

from market_check import MarketCheck


class topicHandler:
    def __init__(self):
        
        pulsar_manager = PulsarManager()
        
        self.topics = pulsar_manager.topics
        
        self.producer = pulsar_manager.create_producer(pulsar_manager.topics.LISTING_TRANSFORM)
        
        self.logs_producer = pulsar_manager.create_producer(pulsar_manager.topics.LOGS)
        
        self.marketcheck = MarketCheck()
        
    def main(self):
        
        status,listings,dealers = self.marketcheck.main()
        
        if status == False:
            return
        
        t1 = datetime.now()
        self.marketcheck.upsert_dealers(dealers)
        listing_ids = self.marketcheck.upsert_listings(listings)
        t2 = datetime.now()
        
        print(f'total time : {(t2 - t1).seconds}')
        
        for id in listing_ids:
            print(id)
            self.producer.produce_message({
                "id":id
            })


if __name__ == "__main__":
    th = topicHandler()
    th.main()