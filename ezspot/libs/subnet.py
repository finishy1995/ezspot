import boto3
from availability_zone import describe_availability_zones
from vpc import describe_default_vpc

def describe_subnet(client, availability_zone='', vpc_id=''):
    if availability_zone == '':
        availability_zone = describe_availability_zones(client)[0]
    if vpc_id == '':
        vpc_id = describe_default_vpc(client)

    response = client.describe_subnets(
        Filters=[ {
            'Name': 'availabilityZone',
            'Values': [
                availability_zone,
            ]
        }, {
            'Name': 'vpc-id',
            'Values': [
                vpc_id,
            ]
        } ],
    )
    
    return response.get('Subnets', [{}])[0].get('SubnetId', '')
