import logger
import time
from aws_client import call
from aws_client import error_handler
from aws_client import get_waiter
from instance import get_specification
from instance import terminate_instances
from instance import create_tag
from instance import instance_wait_until_running
from elastic_ip import create_eip
from elastic_ip import delete_eip

client = 'ec2'

def start_persistent_instances(config, index):
    tag = config.get_arr_attr('wld_fleet_tag', index)
    block_duration = config.get_arr_attr('wld_block_duration', index)
    if not block_duration:
        block_duration = 360
    else:
        block_duration = block_duration
    request_ids = _request(config, index, 'persistent', block_duration)
    logger.info('Request spot instances successfully. Request IDs : ' + str(request_ids))
    time.sleep(5)
    
    _wait_until_completed(request_ids)
    _create_tag(request_ids, tag)
    instances_ids = _describe_request(request_ids)
    
    create_tag(instances_ids, tag)
    instance_wait_until_running(instances_ids)
    eip_arr = create_eip(instances_ids, tag)
    
    logger.info('Spot instances ready.')
    logger.info('Instances public IP: ' + str(eip_arr))
    
def cancel_persistent_instances(config, index):
    tag = config.get_arr_attr('wld_fleet_tag', index)
    request_ids = _describe_request_by_tag(tag)
    logger.info('Get spot instance request ids successfully. Request IDs : ' + str(request_ids))
    status = cancel_spot_request(request_ids, 'Can not cancel spot instance requests, please remember to delete it in your AWS console.')
    
    if status:
        logger.info('Cancel spot instance requests successfully.')
        delete_eip(tag)
    else:
        error_handler('Can not cancel spot instance requests.', 'Failed to cancel spot instances')
    
    logger.info('Spot instances all clear.')
    
def _request(config, index, host_type='one-time', block_duration=360):
    response = call(
        client,
        'request_spot_instances',
        'Request spot instances \'' + config.get_arr_attr('wld_fleet_tag', index) + '\'.',
        _runback_spot_request,
        InstanceCount=config.wld_instance_capacity[index],
        LaunchSpecification=get_specification(config, index, 'spot_instance'),
        Type=host_type,
        BlockDurationMinutes=block_duration
    )

    return _get_request_ids_from_response(response)
        
def _get_request_ids_from_response(response):
    requests = response.get('SpotInstanceRequests', [])
    if requests == []:
        error_handler('Can not request spot instances.', 'Failed to request spot instances.')
    else:
        request_ids = []
        for request in requests:
            request_id = request.get('SpotInstanceRequestId', None)
            if request_id:
                request_ids.append(request_id)
            else:
                error_handler('Can not get request id for spot instances.', 'Failed to request spot instances.')
                
        return request_ids
    
def _runback_spot_request(response):
    error_message = 'Can not delete spot instances, please remember to delete it in your AWS console.'
    request_ids = _get_request_ids_from_response(response)
    
    cancel_spot_request(request_ids, error_message)

def cancel_spot_request(request_ids, error_message, wite_instances=True):
    response = call(
        client,
        'cancel_spot_instance_requests',
        'Cancel spot instances request : ' + str(request_ids),
        SpotInstanceRequestIds=request_ids,
    )

    flag = True
    if response.get('CancelledSpotInstanceRequests', []) == []:
        logger.error(error_message)
        flag = False
    
    if wite_instances:
        instances_ids = _describe_request(request_ids)
        status = terminate_instances(instances_ids)
        if flag and not status:
            flag = status
        
    return flag

def _wait_until_completed(request_ids):
    waiter = get_waiter(client, 'spot_instance_request_fulfilled')
    return waiter.wait(SpotInstanceRequestIds=request_ids)

def _describe_request(request_ids):
    response = call(
        client,
        'describe_spot_instance_requests',
        'Describe spot instance request by id : ' + str(request_ids),
        SpotInstanceRequestIds=request_ids,
    )

    requests = response.get('SpotInstanceRequests', [])
    if requests == []:
        error_handler('Can not describe spot instances.', 'Failed to describe spot instances.')
    else:
        instances_ids = []
        for request in requests:
            instance_id = request.get('InstanceId', None)
            if instance_id:
                instances_ids.append(instance_id)
            else:
                error_handler('Can not get instance id for spot instances.', 'Failed to describe spot instances.')
                
        return instances_ids

def _describe_request_by_tag(tag):
    response = call(
        client,
        'describe_spot_instance_requests',
        'Describe spot instance requests by tag : ' + tag,
        Filters=[ {
            'Name': 'tag-key',
            'Values': [
                'EZSpot',
            ]
        }, {
            'Name': 'tag-value',
            'Values': [
                tag,
            ]
        } ]
    )
    
    return _get_request_ids_from_response(response)

def _create_tag(request_ids, tag):
    if tag:
        call(
            client,
            'create_tags',
            'Create tags for spot instance requests : ' + str(request_ids),
            Resources=request_ids,
            Tags=[ {
                'Key': 'EZSpot',
                'Value': tag
            } ]
        )
    else:
        error_handler('Unsupported tag type : None.', 'Failed to create spot instance requests tag.')
