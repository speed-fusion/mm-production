class MarketCheckFieldMaper:
    def __init__(self) -> None:
        
        self.field_map = [
            {'key': 'source_id', 'value': 'sourceId'},
            {'key': 'source_url', 'value': 'sourceUrl'},
            {'key': 'account_id', 'value': 'Account_ID'},
            {'key': 'website_id', 'value': 'Website_ID'},
            {'key': 'featured_id', 'value': 'Featured_ID'},
            {'key': 'plan_id', 'value': 'Plan_ID'},
            {'key': 'priority', 'value': 'Priority'},
            {'key': 'admin_fee', 'value': 'admin_fees'},
            {'key': 'body_style', 'value': 'body_style'},
            {'key': 'built', 'value': 'built'},
            {'key': 'cab_type', 'value': 'cabType'},
            {'key': 'dealer_id', 'value': 'dealer_id'},
            {'key': 'dealer_location', 'value': 'dealer_location'},
            {'key': 'dealer_name', 'value': 'dealer_name'},
            {'key': 'dealer_phone', 'value': 'dealer_number'},
            {'key': 'doors', 'value': 'doors'},
            {'key': 'emission_scheme', 'value': 'emission_scheme'},
            {'key': 'engine_cylinders_cc', 'value': 'engineCylindersCC'},
            {'key': 'engine_cylinders_litre', 'value': 'engine_cylinders'},
            {'key': 'fuel_code', 'value': 'fuel'},
            {'key': 'location', 'value': 'location_json'},
            {'key': 'predicted_make', 'value': 'make'},
            {'key': 'predicted_model', 'value': 'model'},
            {'key': 'mileage', 'value': 'mileage'},
            {'key': 'price_indicator', 'value': 'price_indicator'},
            {'key': 'predicted_registration', 'value': 'registration'},
            {'key': 'category_id', 'value': 'Category_ID'},
            {'key': 'seats', 'value': 'seats'},
            {'key': 'source_mrp', 'value': 'sourcePrice'},
            {'key': 'title', 'value': 'title'},
            {'key': 'transmission_code', 'value': 'transmission'},
            {'key': 'transmission', 'value': 'transmission_org'},
            {'key': 'trim', 'value': 'trim'},
            {'key': 'vehicle_type', 'value': 'vehicle_type'},
            {'key': 'margin', 'value': 'margin'},
            {'key': 'mm_price', 'value': 'mmPrice'},
            {'key': 'cc_extra_margin', 'value': 'cc_extra_margin'},
            {'key': 'forecourt_110', 'value': 'forecourt_110'},
            {'key': 'registration_date', 'value': 'registration_date'},
            {'key': 'total_photos', 'value': 'Photos_count'},
            {'key':'source_url','value':'sourceUrl'},
            {'key':'source_url','value':'product_url'}
            ]
        
        # self.field_map = {
        #     "source_id":"sourceId",
        #     "source_url":"product_url",
        #     "account_id":"Account_ID",
        #     "website_id":"Website_ID",
        #     "featured_id":"Featured_ID",
        #     "plan_id":"Plan_ID",
        #     "priority":"Priority",
        #     "admin_fee":"admin_fees",
        #     "body_style":"body_style",
        #     "built":"built",
        #     "cab_type":"cabType",
        #     "dealer_id":"dealer_id",
        #     "dealer_location":"dealer_location",
        #     "dealer_name":"dealer_name",
        #     "dealer_phone":"dealer_number",
        #     "doors":"doors",
        #     "emission_scheme":"emission_scheme",
        #     "engine_cylinders_cc":"engineCylindersCC",
        #     "engine_cylinders_litre":"engineCylindersLitre",
        #     "engine_cylinders_litre":"engine_cylinders",
        #     "fuel_code":"fuel",
        #     "location":"location_json",
        #     "predicted_make":"make",
        #     "predicted_model":"model",
        #     "mileage":"mileage",
        #     "price_indicator":"price_indicator",
        #     "predicted_registration":"registration",
        #     "category_id":"Category_ID",
        #     "seats":"seats",
        #     "source_mrp":"sourcePrice",
        #     "title":"title",
        #     "transmission_code":"transmission",
        #     "transmission":"transmission_org",
        #     "trim":"trim",
        #     "vehicle_type":"vehicle_type",
        #     "margin":"margin",
        #     "mm_price":"mmPrice",
        #     "cc_extra_margin":"cc_extra_margin",
        #     "forecourt_110":"forecourt_110",
        #     "registration_date":"registration_date",
        #     "emission_scheme":"emission_scheme",
        #     "total_photos":"Photos_count",
        #     "source_url":"sourceUrl"
        # }
    
    def map(self,data):
        tmp = {}
        
        
        for key in data:
            for item in self.field_map:
                if item["key"] == key:
                    tmp[item["value"]] = data[key]
        
        if "ltv" in data:
            ltv = data["ltv"]
            for key in ltv:
                tmp[key] = ltv[key]

        if "pcp_apr" in data:
            pcp_apr = data["pcp_apr"]
            for key in pcp_apr:
                tmp[key] = pcp_apr[key]
        
        return tmp