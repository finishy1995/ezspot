from aws_client import call
from aws_client import error_handler
import logger

client = 'ec2'

def create_eip(instances, tag):
    elastic_ip_arr = []
    
    for instance in instances:
        response = _allocate_address()
        if response['PublicIp'] and response['AllocationId']:
            elastic_ip_arr.append(response['PublicIp'])
            _tag_address(response['AllocationId'], tag)
            _associate_address(response['AllocationId'], instance['InstanceId'])
        else:
            error_handler('Allocate public IP failed.', 'Failed to create EIP for spot instances.')
        
    return elastic_ip_arr

def delete_eip(tag):
    response = _describe_addresses(tag)
    eips = response.get('Addresses', [])
    
    if eips != []:
        for eip in eips:
            _disassociate_address(eip.get('AssociationId', None))
            _release_address(eip.get('AllocationId', None))
    else:
        error_handler('Describe public IP failed.', 'Failed to delete EIP from spot instances.')

def _tag_address(allocation_id, tag):
    call(
        client,
        'create_tags',
        'Create tags to EIP.',
        Resources=[
            allocation_id
        ],
        Tags=[ {
            'Key': 'EZSpot',
            'Value': tag
        } ]
    )

def _associate_address(allocation_id, instance_id):
    call(
        client,
        'associate_address',
        "Associate EIP to instance: {0}".format(instance_id),
        _runback_disassociate_address,
        AllocationId=allocation_id,
        InstanceId=instance_id,
    )
    
def _runback_disassociate_address(response):
    association_id = response.get('AssociationId', None)
    
    if association_id:
        call(
            client,
            'disassociate_address',
            'Disassociate EIP from instance.',
            AssociationId=association_id
        )
    else:
        logger.error('Can not disassociate EIP, please remember to disassociate it in your AWS console.')

def _allocate_address():
    response = call(
        client,
        'allocate_address',
        'Allocate EIP for spot instances',
        _runback_release_address,
        Domain='vpc',
    )
    
    newResponse = {}
    newResponse['PublicIp'] = response.get('PublicIp', None)
    newResponse['AllocationId'] = response.get('AllocationId', None)
    
    return newResponse
    
def _runback_release_address(response):
    allocation_id = response.get('AllocationId', None)
    
    if allocation_id:
        call(
            client,
            'release_address',
            "Release EIP : {0}.".format(response.get('PublicIp', '')),
            AllocationId=allocation_id
        )
    else:
        logger.error('Can not release eip, please remember to release it in your AWS console.')

def _describe_addresses(tag):
    return call(
        client,
        'describe_addresses',
        'Describe EIP by tag: ' + tag,
        Filters=[ {
            'Name': 'tag-key',
            'Values': ['EZSpot']
        }, {
            'Name': 'tag-value',
            'Values': [tag]
        } ]
    )

def _disassociate_address(association_id):
    if association_id:
        call(
            client,
            'disassociate_address',
            'Disassociate EIP from instance.',
            AssociationId=association_id
        )
    else:
        error_handler('Disassociate public IP failed.', 'Failed to delete EIP from spot instances.')

def _release_address(allocation_id):
    if allocation_id:
        call(
            client,
            'release_address',
            'Release EIP.',
            AllocationId=allocation_id
        )
    else:
        error_handler('Release public IP failed.', 'Failed to delete EIP from spot instances.')
