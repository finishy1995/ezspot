#coding:utf-8

class AvailabilityZone:
    def __init__(self, zone_name, price_history, client):
        self.zone_name = zone_name
        self.price_history = price_history
        
        response = client.describe_regions()
        self.regions_len = len(response['Regions'])

    @property
    def current_price(self):
        if self.price_history:
            return float(self.price_history[0]['SpotPrice'])
        else:
            return None

    def __repr__(self):
        price = str(self.current_price)
        zone_name = self.zone_name
        symbol = "¥" if self.regions_len == 2 else "$"
        return "%s for %s%s/hr" % (zone_name, symbol, price)
        