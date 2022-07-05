import pulsar
import json
from enum import Enum
import os

URI='pulsar://pulsar'

PIPELINE_NAME = os.environ.get("PIPELINE_NAME","")

class Websites(Enum):
    
    AUTO_TRADER = {
        "website_id":17,
        "account_id":24898,
        "plan_id":26,
        "featured_id":26,
        "priority":109
    }
    
    MARKET_CHECK = {
        "website_id":18,
        "account_id":24899,
        "plan_id":27,
        "featured_id":27,
        "priority":110
    }



class Topics(Enum):
    LOGS = "motormarket.scraper.logs"
    
    FL_LISTINGS_UPDATE = f'motormarket{PIPELINE_NAME}.database.fllistings.update'
    
    FL_LISTINGS_INSERT = f'motormarket{PIPELINE_NAME}.database.fllistings.insert'
    
    FL_LISTINGS_FIND = f'motormarket{PIPELINE_NAME}.database.fllistings.find'
    
    LISTING_TRANSFORM = f'motormarket{PIPELINE_NAME}.scraper.listing.transform'
    
    LISTING_PREVALIDATION = f'motormarket{PIPELINE_NAME}.scraper.listing.prevalidation'
    
    LISTING_POSTVALIDATION = f'motormarket{PIPELINE_NAME}.scraper.listing.postvalidation'
    
    LISTING_POST_CALCULATION= f'motormarket{PIPELINE_NAME}.scraper.listing.postcalculation'
    
    LISTING_PREDICT_MAKEMODEL= f'motormarket{PIPELINE_NAME}.scraper.listing.predict.makemodel'
    
    LISTING_PREDICT_NUMBERPLATE= f'motormarket{PIPELINE_NAME}.scraper.listing.predict.numberplate'
    
    LISTING_PREDICT_SEAT= f'motormarket{PIPELINE_NAME}.scraper.listing.predict.seat'
    
    LISTING_PREDICT_IMAGE= f'motormarket{PIPELINE_NAME}.scraper.listing.predict.image'
    
    FL_LISTING_PHOTOS_INSERT = f'motormarket{PIPELINE_NAME}.database.fllistingphotos.insert'
    
    AT_URLS_UPDATE = 'motormarket.database.aturls.update'
    
    GENERATE_IMAGE = f'motormarket{PIPELINE_NAME}.listing.generate.image'
    
    CAR_CUTTER = f'motormarket{PIPELINE_NAME}.listing.replace.background.image'
    
    AUTOTRADER_LISTING_SCRAPER = f'motormarket{PIPELINE_NAME}.scraper.autotrader.listing.scrape'



class Producer:
    def __init__(self,producer_client) -> None:
        self.producer_client = producer_client
    
    def produce_message(self,data):
        
        self.producer_client.send(
            json.dumps(data).encode("utf-8")
        )


class Parser:
    def json_parser(self,message):
        return json.loads(message.data())
    


class Consumer:
    def __init__(self,consumer_client) -> None:
        self.consumer_client = consumer_client
        self.parser = Parser()
        self.websites = Websites()
        
    def print(self,message):
        print(message)
    
    def consume_message(self,timeout_millis = None):
        try:
            message = self.consumer_client.receive(timeout_millis = timeout_millis)
            self.consumer_client.acknowledge(message)
            self.print(f'message_id : {message.message_id()}')
            return self.parser.json_parser(message)
        except:
            return None


class PulsarManager:
    def __init__(self):
        self.topics = Topics
        self.uri =  URI
        self.client = pulsar.Client(self.uri)
        
    def create_producer(self,topic:Topics):
        return Producer(self.client.create_producer(topic.value))
    
    def create_consumer(self,topic:Topics):
        return Consumer(self.client.subscribe(topic.value,f'{topic.name}-subscription',pulsar.ConsumerType.Shared))