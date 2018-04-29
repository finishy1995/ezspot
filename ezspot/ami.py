import boto3

ami_name = 'amzn-ami-hvm-2017.09.1.20171103-x86_64-gp2'

def get_ami_id(client):
    response = client.describe_images(
        Filters=[ {
          'Name': 'name',
            'Values': [
                ami_name
            ]  
        } ],
        Owners=[
            'amazon'
        ]
    )
    
    return response.get('Images')[0].get('ImageId')
