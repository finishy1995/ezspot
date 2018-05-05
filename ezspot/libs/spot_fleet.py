import time
import datetime
import logger
from aws_client import call
from aws_client import error_handler
from elastic_ip import create_eip
from elastic_ip import delete_eip
from price import get_fleet_price
from instance import get_specification

client = 'ec2'

def start_fleet(config, index):
    request_id = _request(config, index)
    if request_id:
        logger.info('Request spot fleet successfully. Request ID : ' + request_id)
    else:
        error_handler('Request spot fleet failed.', 'Failed to get a new spot fleet id.')
    time.sleep(5)
    
    _wait_until_completed(request_id)
    instances_ids = _describe_fleet_instances(request_id)
    eip_arr = create_eip(instances_ids, config.get_arr_attr('wld_fleet_tag', index))
    
    logger.info('Spot fleet ready.')
    logger.info('Instances public IP: ' + str(eip_arr))
    
def cancel_fleet(config, index):
    request_id = _get_fleet_request_id(config, index)
    
    if request_id:
        logger.info('Get fleet request id successfully. Request ID : ' + request_id)
        response = cancel_fleet_request(request_id)
        
        if response.get('UnsuccessfulFleetRequests', []) == []:
            logger.info('Cancel fleet request successfully.')
            delete_eip(config.get_arr_attr('wld_fleet_tag', index))
        else:
            error_handler('Cancel fleet request failed, please check your config.', 'Get the following response: ' + str(response.get('UnsuccessfulFleetRequests', [])))
    else:
        logger.error('Cancel fleet request failed, please check your config.')
        
    logger.info('Spot fleet cancelled.')

def fleet_status(config, index):
    request_id = _get_fleet_request_id(config, index)
    
    if request_id:
        end_time = datetime.datetime.now()
        price_info = _get_fleet_request_price(config, index, request_id, end_time)
        fleet_price = price_info[0] * config.wld_instance_capacity[index]
        
        if price_info:
            logger.info("Now, your spot fleet price is about {0}, run {1} seconds (about {2} hours).".format(fleet_price, price_info[1], price_info[2]))
        else:
            logger.error("Can not get spot fleet price.")
        
        return fleet_price
    else:
        logger.error('Get fleet status failed, please check your config.')

def _request(config, index):
    specification_arr = []
    specification_arr.append(get_specification(config, index))
    
    response = call(
        client,
        'request_spot_fleet',
        'Request spot fleet \'' + config.get_arr_attr('wld_fleet_tag', index) + '\'.',
        _runback_fleet_request,
        SpotFleetRequestConfig = {
            'IamFleetRole': config.wld_iam_role,
            'TargetCapacity': config.wld_instance_capacity[index],
            'TerminateInstancesWithExpiration': False,
            'LaunchSpecifications': specification_arr,
            'ReplaceUnhealthyInstances': False
        } )

    return response.get('SpotFleetRequestId', None)
    
def _runback_fleet_request(response):
    error_message = 'Can not delete spot fleet, please remember to delete it in your AWS console.'
    request_id = response.get('SpotFleetRequestId', None)
    
    if not request_id:
        logger.error(error_message)
    else:
        response = cancel_fleet_request(request_id)
        if response.get('UnsuccessfulFleetRequests', []) != []:
            logger.error(error_message)

def _wait_until_completed(request_id):
    for index in xrange(40):
        response = call(
            client,
            'describe_spot_fleet_requests',
            "Describe spot fleet request: {0} status.".format(request_id),
            SpotFleetRequestIds=[request_id]
        )
        
        status = response.get('SpotFleetRequestConfigs', [{}])[0].get('ActivityStatus', '')
        
        if status == 'error':
            error_handler("Can not start spot fleet {0} now. Please check your config.".format(request_id), 'Failed to request a spot fleet.')
        elif status == 'pending_fulfillment' or status == '':
            logger.info('Please waiting for spot fleet request confirmed ...')
            time.sleep(15)
        elif status == 'fulfilled':
            logger.info("Spot fleet {0} has fulfilled.".format(request_id))
            return
        else:
            error_handler("Unsupported spot fleet request status: {0}.".format(status), 'Failed to request a spot fleet.')

def _describe_fleet_instances(request_id):
    response = call(
        client,
        'describe_spot_fleet_instances',
        "Describe spot fleet instances, spot request: {0}".format(request_id),
        SpotFleetRequestId=request_id
    )
    
    instances = response.get('ActiveInstances', [])
    
    if instances != []:
        instances_ids = []
        for instance in instances:
            instance_id = instance.get('InstanceId', None)
            if instance_id:
                instances_ids.append(instance_id)
            else:
                error_handler('Get wrong intance response.', 'Failed to get spot instances information.')
                
        return instances_ids
    else:
        error_handler('Describe spot fleet instances failed.', 'Failed to get spot instances information.')
    
def _get_fleet_request_id(config, index):
    response = call(
        client,
        'describe_spot_fleet_requests',
        'Describe spot fleet requests.',
    )
    
    request_configs = response.get('SpotFleetRequestConfigs', [])
    if request_configs != []:
        for item in request_configs:
            if item.get('ActivityStatus', '') == 'pending_fulfillment' or item.get('ActivityStatus', '') == 'fulfilled':
                specification = item.get('SpotFleetRequestConfig', {}).get('LaunchSpecifications', [])
                if len(specification) == 1:
                    tags = specification[0].get('TagSpecifications', [])
                    if len(tags) == 1 and tags[0]['Tags'][0]['Key'] == 'EZSpot' and tags[0]['Tags'][0]['Value'] == config.wld_fleet_tag[index]:
                        return item.get('SpotFleetRequestId', None)
    
    return None
    
def cancel_fleet_request(request_id):
    return call(
        client,
        'cancel_spot_fleet_requests',
        'Cancel fleet request : ' + request_id,
        SpotFleetRequestIds=[request_id],
        TerminateInstances=True
    )
    
def _get_fleet_request_price(config, index, request_id, end_time):
    response = call(
        client,
        'describe_spot_fleet_requests',
        'Describe spot fleet request. Request ID: ' + request_id,
        SpotFleetRequestIds=[request_id]
    )
    
    start_time = response.get('SpotFleetRequestConfigs', [{}])[0].get('CreateTime', None)
    return get_fleet_price(start_time, end_time, config.get_arr_attr('wld_instance_type', index), config.prc_product_description)
    
def _describe_fleet_instance_history(client, request_id):
    print (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
    
    return client.describe_spot_fleet_request_history(
        EventType='instanceChange',
        SpotFleetRequestId=request_id,
        StartTime=(datetime.datetime.now() - datetime.timedelta(days=1)),
    )
    