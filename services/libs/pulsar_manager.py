import pulsar
import json
from mm_constants import Topics,PULSAR_HOST


class Producer:
    def __init__(self,producer_client) -> None:
        self.producer_client = producer_client
    
    def produce_message(self,data):
        listing_id = data.get("listing_id",None)
            
        if listing_id != None:
            print(f'sending message to next service : {listing_id}')
        else:
            print(f'listing id not present in message')
        self.producer_client.send(
            json.dumps(data,default=str).encode("utf-8")
        )

class Parser:
    def json_parser(self,message):
        return json.loads(message.data())
    


class Consumer:
    def __init__(self,consumer_client) -> None:
        self.consumer_client = consumer_client
        self.parser = Parser()
        
    def print(self,message):
        print(message)
    
    def consume_message(self,timeout_millis = None):
        try:
            message = self.consumer_client.receive(timeout_millis = timeout_millis)
            self.consumer_client.acknowledge(message)
            json_data = self.parser.json_parser(message)
            listing_id = json_data.get("listing_id",None)
            
            if listing_id != None:
                print(f'received new message : {listing_id}')
            else:
                print(f'listing id not present in message')
                
            return self.parser.json_parser(message)
        except:
            return None


class PulsarManager:
    def __init__(self):
        self.topics = Topics
        self.uri =  PULSAR_HOST
        self.client = pulsar.Client(self.uri)
        
    def create_producer(self,topic:Topics):
        return Producer(self.client.create_producer(topic.value))
    
    def create_consumer(self,topic:Topics):
        return Consumer(self.client.subscribe(topic.value,f'{topic.name}-subscription',pulsar.ConsumerType.Shared))