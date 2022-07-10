from admin_fee import MarketCheckAdminFee

from pcp_apr import MarketCheckPcpAprCalculation

from ltv import LtvCalculationRules

from dealer_forecourt import DealerForecourt

import json

class MarketCheckCalculation:
    
    def __init__(self) -> None:
        
        self.mc_admin_fee = MarketCheckAdminFee()
        
        self.mc_pcp_apr = MarketCheckPcpAprCalculation()
        
        self.mc_ltv = LtvCalculationRules()
        
        self.dealer_forecourt = DealerForecourt()
        
    
    def update_admin_fee(self,data):
        
        dealer_id = data["dealer_id"]
        
        listing_admin_fee = data["admin_fee"]
        
        dealer_admin_fee = self.mc_admin_fee.get_admin_fee(dealer_id)
        
        if dealer_admin_fee > listing_admin_fee:
            data["admin_fee"] = dealer_admin_fee
        
    
    def calculate_source_mrp(self,data):
        
        source_price = data["source_price"]
        
        admin_fee = data["admin_fee"]
        
        data["source_mrp"] = source_price + admin_fee
    
    
    def calculate_margin(self,data):
        
        fixed_margin = 1299
        
        data["margin"] = fixed_margin
    
    def calculate_motor_market_price(self,data):
        
        custom_price_enabled = data.get("custom_price_enabled",False)
        
        if custom_price_enabled == True:
            custom_price = data["custom_price"]
            data["mm_price"] = custom_price
            source_mrp = data["source_mrp"]
            data["margin"] = custom_price - source_mrp
            return
        
        data["mm_price"] = data["source_mrp"] + data["margin"]
    
    def calculate_pcp_apr(self,data):
        
        mm_price = data["mm_price"]
        
        mileage = data["mileage"]
        
        built = data["built"]
        
        pcp_apr = self.mc_pcp_apr.calculate_apr_pcp(mm_price,mileage,built)
        
        data["pcp_apr"] = pcp_apr
    

    
    def calculate_ltv(self,data):
        
        mm_price = data["mm_price"]
        
        source_mrp = data["source_mrp"]
        
        registration_status = data["registration_status"]
        
        registration = data["registration"]
        
        mileage = data["mileage"]
        
        website_id = data["website_id"]
        
        ltv = {}
        
        if source_mrp < 10000:
            if registration_status == True:
                forecourt_price,response = self.dealer_forecourt.get_dealerforecourt_price(registration,mileage,website_id)
                if forecourt_price == None:
                    ltv["ltvStatus"] = 0
                    ltv["dealer_forecourt_response"] = json.dumps(response)
                    ltv["status"] = "approval"
                    ltv.update(self.ltvCalc.getNullValues())
                else:
                    ltv = self.ltvCalc.calculate(mm_price,forecourt_price)
                    ltv["dealerForecourtPrice"] = forecourt_price
                    ltv["ltvStatus"] = 1
            else:
                ltv["ltvStatus"] = 0
                ltv.update(self.ltvCalc.getNullValues())
        else:
            ltv = self.ltvCalc.getDefaultValues()
            ltv["ltvStatus"] = 2
        
        data["ltv"] = ltv
    
    
    
    def calculate_category_id(self,data):
        make = data["make"]
        model = data["model"]
        
        category_id = self.categoryIdCalc.getCategoryId(make,model)
        
        data["category_id"] = category_id
    
    