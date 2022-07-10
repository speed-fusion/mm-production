class MarketCheckValidation:
    def __init__(self) -> None:
        print("validation init")
        
    def validate(self,data):
        
        source_mrp = data["source_mrp"]
        engine_cc = data["engine_cylinders_cc"]
        built = data["built"]
        mileage = data["mileage"]
        dealer_id = data["dealer_id"]
        
        images = data["downloaded_images"]
        
        log = {}
        
        status,message = self.imageValidation(images)
        
        if status == False:
            log["errorMessage"] = message
            
            self.logsProducer.produce_message({
                    "eventType":"insertLog",
                    "data":log
                })
            
            return False
        
        return True
        

    
    def imageValidation(self,images):
        if len(images) == 0:
            return False,"there are no images."
        
        return True,None