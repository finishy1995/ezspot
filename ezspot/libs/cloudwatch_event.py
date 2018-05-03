import boto3




def _put_instance_terminated_rule(client, name):
    response = client.put_rule(
        Name=name,
        EventPattern={
            "source": [ "aws.ec2" ],
            "detail-type": [ "EC2 Instance State-change Notification" ],
            "detail": {
                "state": [ "terminated" ]
            }
        },
        State='ENABLED',
    )
    
    return response.get('RuleArn', '')
    
def _put_instance_terminated_target(client, name, lambda_arn):
    response = client.put_targets(
        Rule=name,
        Targets=[ {
            'Id': 'AWS Lambda functions',
            'Arn': lambda_arn
        } ]
    )
    
    