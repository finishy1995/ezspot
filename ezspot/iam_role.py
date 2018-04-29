import boto3

def get_fleet_role(client):
    name = 'AWSServiceRoleForEC2SpotFleet'
    
    return _get_role(client, name)

def _get_role(client, name):
    response = client.get_role(
        RoleName=name
    )

    return response.get('Role').get('Arn')
