import boto3

def associate_eip(client, instances, tag):
    elastic_ip_arr = []
    
    for instance in instances:
        response = _allocate_address(client)
        elastic_ip_arr.append(response['PublicIp'])
        _tag_address(client, response['AllocationId'], tag)
        _associate_address(client, response['AllocationId'], instance['InstanceId'])
        
    return elastic_ip_arr

def disassociate_eip(client, tag):
    response = _describe_addresses(client, tag)
    eips = response.get('Addresses', [])
    
    for eip in eips:
        _disassociate_address(client, eip.get('AssociationId'))
        _release_address(client, eip.get('AllocationId'))

def _tag_address(client, allocation_id, tag):
    client.create_tags(
        Resources=[
            allocation_id
        ],
        Tags=[ {
            'Key': 'EZSpot',
            'Value': tag
        } ]
    )

def _associate_address(client, allocation_id, instance_id):
    client.associate_address(
        AllocationId=allocation_id,
        InstanceId=instance_id,
    )

def _allocate_address(client):
    response = client.allocate_address(
        Domain='vpc',
    )
    
    newResponse = {}
    newResponse['PublicIp'] = response.get('PublicIp', '')
    newResponse['AllocationId'] = response.get('AllocationId', '')
    
    return newResponse

def _describe_addresses(client, tag):
    return client.describe_addresses(
        Filters=[ {
            'Name': 'tag-key',
            'Values': ['EZSpot']
        }, {
            'Name': 'tag-value',
            'Values': [tag]
        } ]
    )

def _disassociate_address(client, association_id):
    client.disassociate_address(
        AssociationId=association_id
    )

def _release_address(client, allocation_id):
    client.release_address(
        AllocationId=allocation_id
    )
