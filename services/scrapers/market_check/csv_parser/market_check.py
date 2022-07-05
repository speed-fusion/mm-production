import sys

sys.path.append("/libs")

from mongo_database import MongoDatabase

from mm_constants import Websites

import json
from pathlib import Path
import shutil
import pandas as pd
import numpy as np



class MarketCheck:
    
    def __init__(self) -> None:
        
        self.cwd = Path.cwd()
        
        self.new_files_dir = self.cwd.joinpath("new_files")
        
        self.processed_files_dir = self.cwd.joinpath("processed_files")
        
        if not self.new_files_dir.exists():
            self.new_files_dir.mkdir()
        
        if not self.processed_files_dir.exists():
            self.processed_files_dir.mkdir()
        
        self.website_constants = Websites.MARKET_CHECK.value
        
        self.account_id = self.website_constants["account_id"]
    
        self.plan_id = self.website_constants["plan_id"]
        
        self.featured_id = self.website_constants["featured_id"]
        
        self.website_id = self.website_constants["website_id"]
        
        self.priority = self.website_constants["priority"]
        
        self.mongodb = MongoDatabase()
        
    def parse_dealers(self,df:pd.DataFrame):
        columns = ["dealer_id","seller_name","fca_status","fca_reference_no","seller_phone","street","city","county","postal_code","latitude","longitude","country"]
        dealer_df = df[columns]
        dealer_df.drop_duplicates(inplace=True)
        dealer_df.fillna(None,inplace=True)
        for index,row in dealer_df.iterrows():
            row_dict = row.to_dict()
            tmp = {}
            
            tmp["dealer_id"] = row_dict["dealer_id"]
            tmp["dealer_name"] = row_dict["seller_name"]
            tmp["fca_status"] = row_dict["fca_status"]
            tmp["fca_reference_no"] = row_dict["fca_reference_no"]
            tmp["dealer_phone"] = row_dict["seller_phone"]
            tmp["street"] = row_dict["street"]
            tmp["city"] = row_dict["city"]
            tmp["county"] = row_dict["county"]
            tmp["postal_code"] = row_dict["postal_code"]
            tmp["latitude"] = row_dict["latitude"]
            tmp["longitude"] = row_dict["longitude"]
            tmp["country"] = row_dict["country"]
            
            yield tmp
            
    def parse_engine_size(self,text):
        try:
            tmp = float(text.replace("L","").strip())
            return int(tmp * 1000)
        except:
            return None
    
    def parse_listings(self,df:pd.DataFrame):
        
        listing_df = df
        listing_df.drop_duplicates(inplace=True)
        listing_df.fillna(None,inplace=True)
        for index,row in listing_df.iterrows():
            try:
                row_dict = row.to_dict()
                tmp = {}
                tmp["source_id"] = row_dict["id"]
                tmp["source_url"] = row_dict["vdp_url"]
                tmp["price"] = row_dict["price"]
                tmp["mileage"] = row_dict["miles"]
                tmp["built"] = row_dict["year"]
                tmp["make"] = row_dict["make"]
                tmp["model"] = row_dict["model"]
                tmp["trim"] = row_dict["variant"]
                tmp["body_style"] = row_dict["body_type"]
                tmp["fuel"] = row_dict["fuel_type"]
                tmp["transmission"] = row_dict["transmission"]
                tmp["doors"] = row_dict["doors"]
                tmp["registration"] = row_dict["vehicle_registration_mark"]
                tmp["registration_date"] = row_dict["vehicle_registration_date"]
                tmp["exterior_color"] = row_dict["exterior_color"]
                tmp["dealer_id"] = row_dict["dealer_id"]
                tmp["dealer_name"] = row_dict["seller_name"]
                tmp["dealer_number"] = row_dict["seller_phone"]
                tmp["dealer_location"] = row_dict["postal_code"]
                
                tmp["cab_type"] = None
                tmp["seats"] = None
                tmp["write_off_category"] = None
                tmp["doors"] = None
                tmp["price_indicator"] = None
                tmp["admin_fee"] = "0"
                tmp["vehicle_type"] = "car"
                
                
                tmp["location"] = json.dumps({
                    "street":row_dict["street"],
                    "city":row_dict["city"],
                    "county":row_dict["county"],
                    "postal_code":row_dict["postal_code"],
                    "country":row_dict["country"]
                })
                
                tmp["dealer_location"] = row_dict["postal_code"]
                tmp["images"] = []
                if type(row_dict["photo_links"]) == str:
                    for i in row_dict["photo_links"].split("|"):
                        if len(i) < 6:
                            continue
                        tmp["images"].append({
                            "url":i
                        })
                
                tmp["engine_cylinders"] = self.parse_engine_size(row_dict["engine_size"])
                tmp["account_id"] = self.account_id
                tmp["website_id"] = self.website_id
                tmp["featured_id"] = self.featured_id
                tmp["plan_id"] = self.plan_id
                tmp["priority"] = self.priority
                
                yield tmp
                
            except Exception as e:
                print(f'error : {str(e)}')
                print(row_dict)
    
    def parse_csv(self,filepath):
        df = pd.read_csv(filepath)
        
        dealers = self.parse_dealers(df)
        
        listings = self.parse_listings(df)
        
        return listings,dealers
    
    def move_file(self,src,dest):
        try:
            shutil.move(src,dest)
        except Exception as e:
            print(f'error : {str(e)}')
    
    def upsert_dealers(self,dealers):
        for dealer in dealers:
            self.mongodb.upsert_dealer_mc(dealer)
    
    def upsert_listings(self,listings):
        for listing in listings:
            self.mongodb.upsert_listings_mc(listing)
    
    
    
    
    def main(self):
        for file in self.new_files_dir.glob("*.csv.gz"):
            
            if file.is_dir() == True:
                print(f'skipping : it is directory : {str(file)}')
                continue
            
            listings,dealers = self.parse_csv(file)
            
            dest_file = self.processed_files_dir.joinpath(file.name)
            
            # self.move_file(str(file),str(dest_file))
            
            return True,listings,dealers

        return False,None,None