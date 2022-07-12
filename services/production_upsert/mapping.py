class MarketCheckFieldMaper:
    def __init__(self) -> None:
        
        self.field_map = {
            "source_id":"sourceId",
            "source_url":"product_url",
            "account_id":"Account_ID",
            "website_id":"Website_ID",
            "featured_id":"Featured_ID",
            "plan_id":"Plan_ID",
            "priority":"Priority",
            "admin_fee":"admin_fees",
            "body_style":"body_style",
            "built":"built",
            "cab_type":"cabType",
            "dealer_id":"dealer_id",
            "dealer_location":"dealer_location",
            "dealer_name":"dealer_name",
            "dealer_phone":"dealer_number",
            "doors":"doors",
            "emission_scheme":"emission_scheme",
            "engine_cylinders_cc":"engineCylindersCC",
            "engine_cylinders_litre":"engineCylindersLitre",
            "engine_cylinders_litre":"engine_cylinders",
            "fuel_code":"fuel",
            "location":"location_json",
            "predicted_make":"make",
            "predicted_model":"model",
            "mileage":"mileage",
            "price_indicator":"price_indicator",
            "predicted_registration":"registration",
            "category_id":"Category_ID",
            "seats":"seats",
            "source_mrp":"sourcePrice",
            "title":"title",
            "transmission_code":"transmission",
            "transmission":"transmission_org",
            "trim":"trim",
            "vehicle_type":"vehicle_type",
            "margin":"margin",
            "mm_price":"mmPrice",
            "cc_extra_margin":"cc_extra_margin",
            "forecourt_110":"forecourt_110",
            "registration_date":"registration_date",
            "emission_scheme":"emission_scheme"
        }
    
    def map(self,data):
        tmp = {}
        
        for key in data:
            if key in self.field_map:
                tmp[self.field_map[key]] = data[key]
        
        if "ltv" in data:
            ltv = data["ltv"]
            for key in ltv:
                tmp[key] = ltv[key]

        if "pcp_apr" in data:
            pcp_apr = data["pcp_apr"]
            for key in pcp_apr:
                tmp[key] = pcp_apr[key]
        
        return tmp