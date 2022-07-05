import pulsar
import json
from mm_constants import Websites,Topics,URI


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