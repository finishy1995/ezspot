import logger
import time
from aws_client import call
from aws_client import error_handler
from aws_client import get_waiter
from elastic_ip import create_eip
from elastic_ip import delete_eip

client = 'ec2'

def start_on_demand_instances(config, index):
    tag = config.get_arr_attr('wld_fleet_tag', index)
    
    instances_ids = _request(config, index)
    logger.info('Request on-demand instances successfully. Instances IDs : ' + str(instances_ids))
    time.sleep(5)
    
    instance_wait_until_running(instances_ids)
    eip_arr = create_eip(instances_ids, tag)
    
    logger.info('On-demand instances ready.')
    logger.info('Instances public IP: ' + str(eip_arr))
    
def cancel_on_demand_instances(config, index):
    tag = config.get_arr_attr('wld_fleet_tag', index)
    instances_ids = _get_instances_ids(tag)
    logger.info('Get on-demand instance ids successfully. Instances IDs : ' + str(instances_ids))
    status = terminate_instances(instances_ids)
    
    if status:
        logger.info('Cancel on-demand instances successfully.')
        delete_eip(tag)
    else:
        error_handler('Can not cancel on-demand instances requests.', 'Failed to cancel on-demand instances.')
    
    logger.info('On-demand instances all clear.')

def _request(config, index):
    kwargs = get_specification(config, index, request_type='on_demand')
    kwargs['MaxCount'] = config.wld_instance_capacity[index]
    kwargs['MinCount'] = config.wld_instance_capacity[index]
    response = call(
        client,
        'run_instances',
        'Run on-demand instances.',
        _runback_on_demand_instances,
        **kwargs
    )
    
    return _get_instances_ids_from_response(response)
        
def _get_instances_ids_from_response(response):
    instances = response.get('Instances', [])
    if instances == []:
        error_handler('Can not request on-demand instances.', 'Failed to request on-demand instances.')
    else:
        instances_ids = []
        for instance in instances:
            instance_id = instance.get('InstanceId', None)
            if instance_id:
                instances_ids.append(instance_id)
            else:
                error_handler('Can not get instance id from response.', 'Failed to request on-demand instances.')
                
        return instances_ids

def _runback_on_demand_instances(response):
    instances_ids = _get_instances_ids_from_response(response)
    
    terminate_instances(instances_ids)

def get_specification(config, index, request_type='spot_fleet'):
    item = {}
    params = {
        'EbsOptimized'  : 'wld_ebs_optimized',
        'ImageId'       : 'wld_instance_ami',
        'InstanceType'  : 'wld_instance_type',
        'KeyName'       : 'wld_instance_key',
        'SubnetId'      : 'wld_instance_subnet',
    }
    for key in params:
        _insert_new_key(config, params[key], index, item, key)
    
    value = config.get_arr_attr('wld_instance_sg', index)
    if value:
        item['SecurityGroups'] = [{ 'GroupId': value }]
    
    if request_type == 'spot_fleet':
        item['WeightedCapacity'] = 1
        
    if request_type == 'spot_fleet' or request_type == 'on_demand':
        value = config.get_arr_attr('wld_fleet_tag', index)
        if value:
            item['TagSpecifications'] = [ {
                'ResourceType': 'instance',
                'Tags': [ {
                    'Key': 'EZSpot',
                    'Value': value
                } ]
            } ]
    
    return item

def terminate_instances(instances_ids):
    response = call(
        client,
        'terminate_instances',
        'Terminate instances : ' + str(instances_ids),
        InstanceIds=instances_ids
    )
    
    if response.get('TerminatingInstances', []) == []:
        logger.warning('Terminate no instances, please check if there is something wrong.')
        return False
    
    return True

def terminate_instances_by_tag(tag):
    if tag:
        instances_ids = _get_instances_ids(tag)
    
        if instances_ids:
            terminate_instances(instances_ids)
        else:
            logger.warning('Not find any instances to terminate.')
    else:
        logger.error('Unsupported tag type : None.')

def create_tag(instances_ids, tag):
    if tag:
        call(
            client,
            'create_tags',
            'Create tags for instances : ' + str(instances_ids),
            Resources=instances_ids,
            Tags=[ {
                'Key': 'EZSpot',
                'Value': tag
            } ]
        )
    else:
        error_handler('Unsupported tag type : None.', 'Failed to create instances tag.')

def instance_wait_until_running(instances_ids):
    waiter = get_waiter(client, 'instance_running')
    return waiter.wait(InstanceIds=instances_ids)

def _insert_new_key(config, attr, index, item, key):
    value = config.get_arr_attr(attr, index)
    
    if value:
        item[key] = value

def _get_instances_ids(tag):
    response = call(
        client,
        'describe_tags',
        "Describe instances which has tag EZSpot : {0}.".format(tag),
        Filters=[ {
            'Name': 'key',
            'Values': [
                'EZSpot',
            ]
        }, {
            'Name': 'value',
            'Values': [
                tag,
            ]
        }, {
            'Name': 'resource-type',
            'Values': [
                'instance',
            ]
        } ],
    )

    tags = response.get('Tags', None)
    instances_ids = []
    
    if tags:
        for item in tags:
            instances_ids.append(item.get('ResourceId', None))
    
    return instances_ids
    