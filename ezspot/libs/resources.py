import logger
from aws_client import call
from spot_fleet import cancel_fleet_request
from spot_instance import cancel_spot_request
from instance import terminate_instances
from elastic_ip import release_address

client = 'ec2'

def clean():
    request_ids = _get_fleet_request_ids()
    for request_id in request_ids:
        if request_id:
            logger.info('Get fleet request id successfully. Request ID : ' + request_id)
            response = cancel_fleet_request(request_id)
            
            if response.get('UnsuccessfulFleetRequests', []) == []:
                logger.info("Cancel fleet request successfully.")
            else:
                logger.error("Cancel fleet request {0} failed.".format(request_id))
                logger.debug('Get the following response: ' + str(response.get('UnsuccessfulFleetRequests', [])))
        else:
            logger.error('Failed to get fleet request id.')
            
    instances_request_ids = _describe_tags('spot-instances-request')
    if instances_request_ids != []:
        logger.info('Get spot instance request ids successfully. Request IDs : ' + str(instances_request_ids))
        status = cancel_spot_request(instances_request_ids, 'Can not cancel spot instance requests, please remember to delete it in your AWS console.', False)
        if status:
            logger.info('Cancel spot instance requests successfully.')
        else:
            logger.error('Failed to cancel spot instances.')
        
    instances_ids = _describe_tags('instance')
    if instances_ids != []:
        logger.info('Get instances ids successfully. Instances IDs : ' + str(instances_ids))
        status = terminate_instances(instances_ids)
        if status:
            logger.info('Cancel instances successfully.')
        else:
            logger.error('Failed to cancel instances.')
        
    eips = _describe_tags('elastic-ip')
    if eips != []:
        logger.info('Get eips successfully. EIPs : ' + str(eips))
        for eip in eips:
            if eip:
                release_address(eip)
            else:
                logger.error('Failed to release eip : ' + eip)
    
    logger.info('All resources clean.')

def _get_fleet_request_ids():
    response = call(
        client,
        'describe_spot_fleet_requests',
        'Describe spot fleet requests.',
    )
    
    request_ids = []
    request_configs = response.get('SpotFleetRequestConfigs', [])
    if request_configs != []:
        for item in request_configs:
            if item.get('ActivityStatus', '') == 'pending_fulfillment' or item.get('ActivityStatus', '') == 'fulfilled':
                specification = item.get('SpotFleetRequestConfig', {}).get('LaunchSpecifications', [])
                if len(specification) == 1:
                    tags = specification[0].get('TagSpecifications', [])
                    if len(tags) == 1 and tags[0]['Tags'][0]['Key'] == 'EZSpot':
                        request_ids.append(item.get('SpotFleetRequestId', None))
    
    return request_ids

def _describe_tags(resource_type):
    response = call(
        client,
        'describe_tags',
        'Describe spot instances request ids.',
        Filters=[ {
           'Name': 'resource-type',
            'Values': [
                resource_type,
            ]
        }, {
            'Name': 'key',
            'Values': [
                'EZSpot',
            ]
        } ]
    )
    
    request_arr = []
    tags = response.get('Tags', [])
    
    for tag in tags:
        request = tag.get('ResourceId', None)
        request_arr.append(request)
    
    return request_arr
    