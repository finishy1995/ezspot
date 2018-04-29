import datetime
import sys
import boto3
from availability_zone import AvailabilityZone

def get_az_arr(config):
    zone_names = _get_zone_names(config.ec2Client)
    instance_type = config.wld_instance_type
    az_arr = []
    
    for index in xrange(len(instance_type)):
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

def _get_price_history(config, zone_name, instance_type):
    response = config.ec2Client.describe_spot_price_history(
        DryRun=False,
        StartTime=datetime.datetime.now() - datetime.timedelta(hours=config.prc_product_timerange),
        EndTime=datetime.datetime.now(),
        InstanceTypes=[instance_type],
        AvailabilityZone=zone_name,
        ProductDescriptions=[config.prc_product_description])
    return response.get('SpotPriceHistory', [])

def _score(az):
    return az.current_price or sys.maxsize
