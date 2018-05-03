import time
import datetime
import logger
from aws_client import call
from aws_client import error_handler
from elastic_ip import create_eip
from elastic_ip import delete_eip

client = 'ec2'

def start_fleet(config, index):
    request_id = _request(config, index)
    if request_id:
        logger.info('Request spot fleet successfully. Request ID : ' + request_id)
    else:
        error_handler('Request spot fleet failed.', 'Failed to get a new spot fleet id.')
    time.sleep(5)
    
    _wait_until_completed(request_id)
    instances = _describe_fleet_instances(request_id)
    
    if instances:
        eip_arr = create_eip(instances, _get_config_arr_attr(config, 'wld_fleet_tag', index))
    else:
        error_handler('Describe spot fleet instances failed.', 'Failed to get spot instances information.')
    
    logger.info('Spot fleet ready.')
    logger.info('Instances public IP: ' + str(eip_arr))
    
def cancel_fleet(config, index):
    request_id = _get_fleet_request_id(config, index)
    
    if request_id:
        logger.info('Get fleet request id successfully. Request ID : ' + request_id)
        response = _cancel_fleet_request(request_id)
        
        if response.get('UnsuccessfulFleetRequests', []) == []:
            logger.info('Cancel fleet request successfully.')
            delete_eip(_get_config_arr_attr(config, 'wld_fleet_tag', index))
        else:
            error_handler('Cancel fleet request failed, please check your config.', 'Get the following response: ' + str(response.get('UnsuccessfulFleetRequests', [])))
    else:
        error_handler('Cancel fleet request failed, please check your config.', 'Failed to get fleet request id.')
        
    logger.info('Spot fleet cancelled.')

def fleet_status(config, index):
    request_id = _get_fleet_request_id(config, index)
    
    if request_id != '':
        response = _describe_fleet_instance_history(config.ec2Client, request_id)
        
        if response.get('HistoryRecords', []) != []:
            return response.get('HistoryRecords')
            
    return False

def _request(config, index):
    specification_arr = []
    specification_arr.append(_get_specification_item(config, index))
    
    response = call(
        client,
        'request_spot_fleet',
        'Request spot fleet \'' + _get_config_arr_attr(config, 'wld_fleet_tag', index) + '\'.',
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
        response = _cancel_fleet_request(request_id)
        if response.get('UnsuccessfulFleetRequests', []) != []:
            logger.error(error_message)

def _get_specification_item(config, index):
    item = {
        'WeightedCapacity': 1,
    }
    params = {
        'EbsOptimized'  : 'wld_ebs_optimized',
        'ImageId'       : 'wld_instance_ami',
        'InstanceType'  : 'wld_instance_type',
        'KeyName'       : 'wld_instance_key',
        'SubnetId'      : 'wld_instance_subnet',
    }
    for key in params:
        _insert_new_key(config, params[key], index, item, key)
    
    value = _get_config_arr_attr(config, 'wld_instance_sg', index)
    if value:
        item['SecurityGroups'] = [{ 'GroupId': value }]
        
    value = _get_config_arr_attr(config, 'wld_fleet_tag', index)
    if value:
        item['TagSpecifications'] = [ {
            'ResourceType': 'instance',
            'Tags': [ {
                'Key': 'EZSpot',
                'Value': value
            } ]
        } ]
    
    return item

def _insert_new_key(config, attr, index, item, key):
    value = _get_config_arr_attr(config, attr, index)
    
    if value:
        item[key] = value

def _get_config_arr_attr(config, attr, index):
    value = getattr(config, attr, None)
    
    if value:
        return value[index]
    else:
        return None

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
    
    return response.get('ActiveInstances', None)
    
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
    
def _cancel_fleet_request(request_id):
    return call(
        client,
        'cancel_spot_fleet_requests',
        'Cancel fleet request : ' + request_id,
        SpotFleetRequestIds=[request_id],
        TerminateInstances=True
    )
    
def _describe_fleet_instance_history(client, request_id):
    print (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
    
    return client.describe_spot_fleet_request_history(
        EventType='instanceChange',
        SpotFleetRequestId=request_id,
        StartTime=(datetime.datetime.now() - datetime.timedelta(days=1)),
    )
    