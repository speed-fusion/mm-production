from enum import Enum
import os

URI='pulsar://pulsar'

PIPELINE_NAME = os.environ.get("PIPELINE_NAME",".default")

class AutoTraderConstants(Enum):
    WEBSITE_ID = 17
    ACCOUNT_ID = 24898
    PLAN_ID = 26
    FEATURED_ID = 26
    PRIORITY = 109

class MarketCheckConstants(Enum):
    WEBSITE_ID = 18
    ACCOUNT_ID = 24899
    PLAN_ID = 27
    FEATURED_ID = 27
    PRIORITY = 110

class Topics(Enum):
    LOGS = "motormarket.scraper.logs"
    
    FL_LISTINGS_UPDATE = f'motormarket{PIPELINE_NAME}.database.fllistings.update'
    
    FL_LISTINGS_INSERT = f'motormarket{PIPELINE_NAME}.database.fllistings.insert'
    
    FL_LISTINGS_FIND = f'motormarket{PIPELINE_NAME}.database.fllistings.find'
    
    LISTING_TRANSFORM = f'motormarket{PIPELINE_NAME}.scraper.listing.transform'
    
    LISTING_PRE_VALIDATION = f'motormarket{PIPELINE_NAME}.scraper.listing.prevalidation'
    
    LISTING_POST_VALIDATION = f'motormarket{PIPELINE_NAME}.scraper.listing.postvalidation'
    
    LISTING_POST_CALCULATION= f'motormarket{PIPELINE_NAME}.scraper.listing.postcalculation'
    
    LISTING_PREDICT_MAKE_MODEL= f'motormarket{PIPELINE_NAME}.scraper.listing.predict.makemodel'
    
    LISTING_PREDICT_NUMBERPLATE= f'motormarket{PIPELINE_NAME}.scraper.listing.predict.numberplate'
    
    LISTING_PREDICT_SEAT= f'motormarket{PIPELINE_NAME}.scraper.listing.predict.seat'
    
    LISTING_PREDICT_CAR_IMAGE= f'motormarket{PIPELINE_NAME}.scraper.listing.predict.car.image'
    
    FL_LISTING_PHOTOS_INSERT = f'motormarket{PIPELINE_NAME}.database.fllistingphotos.insert'
    
    AT_URLS_UPDATE = 'motormarket.database.aturls.update'
    
    GENERATE_IMAGE = f'motormarket{PIPELINE_NAME}.listing.generate.image'
    
    CAR_CUTTER = f'motormarket{PIPELINE_NAME}.listing.replace.background.image'
    
    AUTOTRADER_LISTING_SCRAPER = f'motormarket{PIPELINE_NAME}.scraper.autotrader.listing.scrape'