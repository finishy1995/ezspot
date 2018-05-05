import logger
from aws_client import call
from aws_client import error_handler

client = 'ec2'

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
    