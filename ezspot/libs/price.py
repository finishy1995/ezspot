import datetime
import time
import sys
import logger
from aws_client import call

client = 'ec2'

def get_fleet_price(start_time, current_time, instance_type, product_descriptions):
    response = call(
        client,
        'describe_spot_price_history',
        "Describe spot price history from start time : {0}, instance type: {1}, product: {2}.".format(start_time, instance_type, product_descriptions),
        DryRun=False,
        StartTime=start_time,
        EndTime=current_time,
        InstanceTypes=[instance_type],
        ProductDescriptions=[product_descriptions])
    price_history = response.get('SpotPriceHistory', [])
    
    if len(price_history) == 0:
        logger.debug('Get no price_history from aws spot price history.')
        return None
    else:
        az_list = {}
        for index in xrange(len(price_history) - 1, -1, -1):
            az = price_history[index].get('AvailabilityZone', None)
            price = price_history[index].get('SpotPrice', None)
            if az and price:
                price = float(price)
                if az_list.has_key(az):
                    break
                az_list[az] = price
            else:
                return None
        logger.debug('AZ first price is : ' + str(az_list))
                
        min = sys.maxsize
        min_az = None
        for az in az_list:
            if az_list[az] < min:
                min = az_list[az]
                min_az = az
        logger.debug("Choose AZ : {0} as calculate price az.".format(min_az))
        
        total = 0.0
        peer_time = start_time
        peer_price = 0.0
        logger.debug('Price claculate start at : ' + str(start_time))
        if min_az:
            for index in xrange(len(price_history) - 1, -1, -1):
                if min_az == price_history[index].get('AvailabilityZone', None):
                    price = float(price_history[index].get('SpotPrice', None))
                    timestamp = price_history[index].get('Timestamp', None)
                    if price and timestamp:
                        logger.debug("Get time : {0} at price : {1}.".format(str(timestamp), price))
                        if time.mktime(timestamp.timetuple()) > time.mktime(peer_time.timetuple()):
                            total += peer_price * (time.mktime(timestamp.timetuple()) - time.mktime(peer_time.timetuple())) / 3600
                            peer_time = timestamp
                        
                        peer_price = price
            
            total += peer_price * (time.mktime(current_time.timetuple()) - time.mktime(peer_time.timetuple())) / 3600
            return [total, (time.mktime(current_time.timetuple()) - time.mktime(peer_time.timetuple())), round((time.mktime(current_time.timetuple()) - time.mktime(peer_time.timetuple())) / 3600)]
        else:
            return None

def get_az(config):
    az_arr = _get_az_arr(config)
    az_all = []
    for index in xrange(len(az_arr)):
        az_all.append(az_arr[0])
    
    config.set_azs(az_all)
    return az_arr[0].zone_name

def _get_az_arr(config):
    zone_names = _get_zone_names(config.ec2Client)
    instance_type = config.wld_instance_type
    az_arr = []
    
    for index in xrange(config.wld_fleet_number):
        azs = []
        for zone_name in zone_names:
            price_history = _get_price_history(config, zone_name, instance_type[index])
            azs.append(AvailabilityZone(zone_name, price_history, config.ec2Client))

        az_arr.append(sorted(azs, key=_score)[0])
        
    return az_arr

def _get_zone_names(client):
    zone_names = []
    for zone in client.describe_availability_zones()['AvailabilityZones']:
        if zone['State'] == 'available':
            zone_names.append(zone['ZoneName'])
            
    return zone_names

def _get_price_history(start_time, instance_type, product_descriptions):
    response = call(
        client,
        'describe_spot_price_history',
        DryRun=False,
        StartTime=start_time,
        EndTime=datetime.datetime.now(),
        InstanceTypes=[instance_type],
        ProductDescriptions=[config.prc_product_description])
    return response.get('SpotPriceHistory', [])

def _score(az):
    return az.current_price or sys.maxsize
