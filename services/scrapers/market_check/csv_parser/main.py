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
        
        self.marketcheck.upsert_dealers(dealers)
        
        self.marketcheck.upsert_listings(listings)
        
        
        # for listing in listings:
        #     print(listing)
        #     self.producer.produce_message({
        #         "data":listing
        #     })
            
        #     break


if __name__ == "__main__":
    th = topicHandler()
    th.main()