import boto3

def describe_default_vpc(client):
    response = client.describe_vpcs(
        Filters=[ {
            'Name': 'isDefault',
            'Values': [
                'true',
            ]
        } ],
    )
    
    return response.get('Vpcs', [{}])[0].get('VpcId', '')
