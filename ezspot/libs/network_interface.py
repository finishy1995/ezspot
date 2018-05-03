import boto3
from elastic_ip import create_eip
from elastic_ip import delete_eip
from subnet import describe_subnet

def create_interface(client, tag, subnet_id=''):
    if subnet_id == '' or not subnet_id:
        subnet_id = describe_subnet(client)
    interface_id = _create_network_interface(client, tag, subnet_id)
    _tag_interface(client, tag, interface_id)
    elastic_ip = create_eip(client, interface_id, tag)
    
    return (interface_id, elastic_ip)
    
def delete_interface(client, tag):
    return 'Need to do'

def _create_network_interface(client, tag, subnet_id):
    response = client.create_network_interface(
        Description='EZSpot ' + tag,
        SubnetId=subnet_id
    )

    return response.get('NetworkInterface', {}).get('NetworkInterfaceId', '')

def _tag_interface(client, tag, interface_id):
    client.create_tags(
        Resources=[
            interface_id
        ],
        Tags=[ {
            'Key': 'EZSpot',
            'Value': tag
        } ]
    )
