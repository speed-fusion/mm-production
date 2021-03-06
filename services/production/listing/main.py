import sys

sys.path.append("/libs")

from pulsar_manager import PulsarManager

from mongo_database import MongoDatabase
from mysql_database import MysqlDatabase

from MMUrlGenerator import MMUrlGenerator

from mapping import MarketCheckFieldMaper
class TopicHandler:
    def __init__(self):
        print("transform topic handler init")
        
        pulsar_manager = PulsarManager()
        
        self.consumer = pulsar_manager.create_consumer(pulsar_manager.topics.LISTINGS_UPSERT_PROD_DB)
        
        self.producer = pulsar_manager.create_producer(pulsar_manager.topics.CAR_CUTTER)
        
        self.mongodb = MongoDatabase()
        
        self.mysqldb = MysqlDatabase()
        
        self.urlGenerator = MMUrlGenerator()
        
        self.mc_mapper = MarketCheckFieldMaper()
    
    
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
                mapped_data = self.mc_mapper.map(data)
                
                mapped_data["Status"] = "to_parse"
                
                self.mysqldb.connect()
                try:
                    result = self.mysqldb.recCustomQuery(f'SELECT ID,Status From fl_listings WHERE sourceId={data["source_id"]} AND Website_ID={website_id}')
                    
                    if len(result) == 0:
                        mapped_data["create_ts"] = {"func":"now()"}
                        mapped_data["updated_at"] = {"func":"now()"}
                        
                        id = self.mysqldb.recInsert("fl_listings",mapped_data)
                        
                        make = mapped_data["make"]
                        model = mapped_data["model"]
                        title = mapped_data["title"]
                        
                        mm_url = self.urlGenerator.generateMMUrl(make,model,title,id)
                        
                        self.mongodb.listings_collection.update_one(where,{
                            "$set":{
                                "mysql_listing_id":id,
                                "mm_url":mm_url
                            }
                        })
                    else:
                        status = result[0]["Status"]
                        
                        if status in ["manual_expire","to_parse","pending","sold"]:
                            continue
                        
                        if status == "expired":
                            self.mysqldb.recUpdate("fl_listing",mapped_data,{"ID":result[0]["ID"]})
                            continue
                        
                except Exception as e:
                    print(f'error : {str(e)}')   
                self.mysqldb.disconnect()
                
                
            self.producer.produce_message(message)  
            
        
if __name__ == "__main__":
    topic_handler = TopicHandler()
    topic_handler.main()

