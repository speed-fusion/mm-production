import sys

sys.path.append("/libs")

from mongo_database import MongoDatabase

from helper import clean_string,clean_int,generate_title,generate_sha1,get_current_datetime


class MarketCheckTransform:
    def __init__(self) -> None:
        
        self.mongo_db = MongoDatabase()
        
        self.transmission_codes = {
            "automatic":1,
            "manual":2,
            "automanual":3,
            "auto":1,
            "auto clutch":1,
            "auto/manual mode":1,
            "cvt":1,
            "cvt/manual mode":1,
            "manual transmission":2,
            "semi-automatic":1,
            "sequential":1
        }
        
        self.fuel_codes = {
            "petrol":1,
            "diesel":2,
            "gas":3,
            "hybrid":5,
            "electric":6,
            "hybrid - petrol/elec":7,
            "hybrid":8,
        }
    
    def transform(self,data,listing_id):
        
        raw = data["raw"]
        
        final = {}
        
        dealer_name = raw.get("dealer_name",None)
        final["dealer_name"] = clean_string(dealer_name)
        
        dealer_phone = raw.get("dealer_phone",None)
        final["dealer_phone"] = clean_string(dealer_phone)
        
        dealer_location = raw.get("dealer_location",None)
        final["dealer_location"] = clean_string(dealer_location)
        
        location = raw.get("location",None)
        final["location"] = clean_string(location)
        
        dealer_id = raw.get("dealer_id",None)
        final["dealer_id"] = clean_int(dealer_id)
        
        cab_type = raw.get("cab_type",None)
        final["cab_type"] = clean_string(cab_type)
        
        make = raw.get("make",None)
        final["make"] = clean_string(make)
        
        model = raw.get("model",None)
        final["model"] = clean_string(model)
        
        engine_cylinders_cc = raw.get("engine_cylinders_cc",None)
        final["engine_cylinders_cc"] = clean_int(engine_cylinders_cc)
        
        if engine_cylinders_cc != None:
            final["engine_cylinders_litre"] = round(engine_cylinders_cc/1000,1)
        else:
            final["engine_cylinders_litre"] = None
        
        registration = raw.get("registration",None)
        final["registration"] = clean_string(registration)
        
        if final["registration"] != None:
            final["registration"] = final["registration"].replace(" ","").strip()
        
        built = raw.get("built",None)
        final["built"] = clean_int(built)
        
        seats = raw.get("seats",None)
        final["seats"] = clean_int(seats)
        
        mileage = raw.get("mileage",None)
        final["mileage"] = clean_int(mileage)
        
        fuel = raw.get("fuel",None)
        final["fuel"] = clean_string(fuel)

        write_off_category = raw.get("write_off_category",None)
        final["write_off_category"] = clean_string(write_off_category)
        
        doors = raw.get("doors",None)
        final["doors"] = clean_int(doors)
        
        body_style = raw.get("body_style",None)
        final["body_style"] = clean_string(body_style)
        
        source_price = raw.get("price",None)
        final["source_price"] = clean_int(source_price)
        
        price_indicator = raw.get("price_indicator",None)
        final["price_indicator"] = clean_string(price_indicator)
        
        admin_fee = raw.get("admin_fee",0)
        final["admin_fee"] = clean_int(admin_fee)
        
        trim = raw.get("trim",None)
        final["trim"] = clean_string(trim)
        
        vehicle_type = raw.get("vehicle_type",None)
        final["vehicle_type"] = clean_string(vehicle_type)
        
        emission_scheme = raw.get("emission_scheme",None)
        final["emission_scheme"] = emission_scheme
        
        transmission = raw.get("transmission",None)
        final["transmission"] = clean_string(transmission)
        
        final["images"] = raw.get("images",[])
        
        self.upsert_images(listing_id,final["images"])
        
        final["title"] = generate_title(make,model,trim)
        
        final["transmission_code"] = self.transmission_codes.get(transmission,4)
        
        final["fuel_code"] = self.fuel_codes.get(fuel,4)
        
        final["source_mrp"] = final["source_price"] + final["admin_fee"]
        
        return final
    
    def upsert_images(self,listing_id,images):
        for index,img in enumerate(images):
            url = img["url"]
            id = generate_sha1(url)
            
            where = {"_id":id}
            
            result = self.mongo_db.images_collection.find_one(where)
            
            now = get_current_datetime()
            
            if result == None:
                what = {
                    "url":url,
                    "_id":id,
                    "listing_id":listing_id,
                    "created_at":now,
                    "updated_at":now,
                    "position":index
                }
                
                self.mongo_db.images_collection.insert_one(what)

                continue