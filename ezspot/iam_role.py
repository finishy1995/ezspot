import boto3
import json

basic_lambda_role = {
    "Version": "2012-10-17",
    "Statement": {
        "Effect": "Allow",
        "Principal": {"Service": "lambda.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }
}

eip_handler_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:AssociateAddress",
                "ec2:DescribeAddresses",
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}

def get_fleet_role(client):
    name = 'AWSServiceRoleForEC2SpotFleet'
    
    return _get_role(client, name)

def create_eip_handler_role(client, name):
    arn = _create_role(client, name, basic_lambda_role)
    
    client.put_role_policy(
        RoleName=name,
        PolicyName=name + '-policy',
        PolicyDocument=_get_urlencode(eip_handler_policy)
    )
    
    return arn

def _get_role(client, name):
    response = client.get_role(
        RoleName=name
    )

    return response.get('Role').get('Arn')

def _get_urlencode(policy):
    return json.dumps(policy)

def _create_role(client, name, policy):
    response = client.create_role(
        RoleName=name,
        AssumeRolePolicyDocument=_get_urlencode(policy)
    )

    return response.get('Role', {}).get('Arn', '')
